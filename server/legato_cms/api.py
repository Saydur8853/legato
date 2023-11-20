from django.shortcuts import redirect
from wagtail.api.v2.views import PagesAPIViewSet as WagtailPagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.utils import get_object_detail_url
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from django.contrib.contenttypes.models import ContentType
from wagtail_headless_preview.models import PagePreview
from rest_framework.response import Response
from django.utils.decorators import method_decorator
# from custom_cache_page.cache import cache_page
from django.http import Http404
import logging

logger = logging.getLogger(__name__)


class PagesAPIViewSet(WagtailPagesAPIViewSet):

    def find_view(self, request):
        queryset = self.get_queryset()

        try:
            obj = self.find_object(queryset, request)

            if obj is None:
                raise self.model.DoesNotExist

        except self.model.DoesNotExist:
            raise Http404("not found")

        # Generate redirect
        url = get_object_detail_url(
            self.request.wagtailapi_router, request, self.model, obj.pk)

        if url is None:
            # Shouldn't happen unless this endpoint isn't actually installed in the router
            raise Exception("Cannot generate URL to detail view. Is '{}' installed in the API router?".format(
                self.__class__.__name__))

        if request.query_params.get('redirect', 'true') == 'false':
            request.parser_context["kwargs"]["pk"] = obj.pk
            self.request = request
            serializer = self.get_serializer(obj)
            # logger.critical(serializer.data)
            return Response(serializer.data)
        else:
            return redirect(url)


class PagePreviewAPIViewSet(PagesAPIViewSet):
    known_query_parameters = PagesAPIViewSet.known_query_parameters.union(
        ["content_type", "token"]
    )

    def listing_view(self, request):
        page = self.get_object()
        serializer = self.get_serializer(page)
        return Response(serializer.data)

    def detail_view(self, request, pk):
        page = self.get_object()
        serializer = self.get_serializer(page)
        return Response(serializer.data)

    def get_object(self):
        app_label, model = self.request.GET["content_type"].split(".")
        content_type = ContentType.objects.get(
            app_label=app_label, model=model)

        page_preview = PagePreview.objects.get(
            content_type=content_type, token=self.request.GET["token"]
        )
        page = page_preview.as_page()
        if not page.pk:
            # fake primary key to stop API URL routing from complaining
            page.pk = 0

        return page


# Create the router. "wagtailapi" is the URL namespace
api_router = WagtailAPIRouter("wagtailapi")

# Add the three endpoints using the "register_endpoint" method.
# The first parameter is the name of the endpoint (eg. pages, images). This
# is used in the URL of the endpoint
# The second parameter is the endpoint class that handles the requests
api_router.register_endpoint("pages", PagesAPIViewSet)
api_router.register_endpoint("images", ImagesAPIViewSet)
api_router.register_endpoint("documents", DocumentsAPIViewSet)
api_router.register_endpoint("page_preview", PagePreviewAPIViewSet)