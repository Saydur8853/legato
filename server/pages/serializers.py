from rest_framework import serializers 
from wagtail.models import Site
from wagtailmenus.models import MainMenu 
# from wagtailutils.serializers import MainMenuItemSerializer

class SettingsSerializer(serializers.Serializer):
    pass
    # site = serializers.SerializerMethodField()
    # # footer = serializers.SerializerMethodField()
    # main_menu = serializers.SerializerMethodField()

    # def get_main_menu(self, model):
    #     site = Site.find_for_request(self.context["request"])
    #     try:
    #         main_menu = MainMenu.objects.get(site=site)
    #         # settings = GlobalSettings.for_request(self.context["request"])
    #         main_menu_data = MainMenuItemSerializer(
    #             main_menu.menu_items.all(), context=self.context, many=True
    #         ).data
    #         return {
    #             "menu": main_menu_data,
    #             # "contact_page": settings.contact_page.get_url(self.context["request"]) if settings.contact_page else None,
    #             # "contact_page_label": settings.contact_page_label,
    #         }
    #     except Exception as e:
    #         raise e
        
    # def get_site(self, model):
    #     site = Site.find_for_request(self.context["request"])
    #     # settings = GlobalSettings.for_request(self.context["request"])

    #     return {
    #         "title": site,
    #         # **GlobalSettingsSerializer(settings, context=self.context).data,
    #     }
