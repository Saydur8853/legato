from wagtail import blocks
from wagtailutils.utils import prepare_richtext_for_api
from wagtail.images.blocks import ImageChooserBlock as DefaultImageChooserBlock 
from wagtail.images.views.serve import generate_image_url

class ImageChooserBlock(DefaultImageChooserBlock):
    def to_python(self, value):
        if value is None:
            return value
        else:
            try:
                return (
                    self.target_model.objects.filter(pk=value)
                    .prefetch_related("renditions")
                    .first()
                )
            except self.target_model.DoesNotExist:
                return None

    def get_api_representation(self, value, context=None):
        if value:
            data = {
                "id": value.id,
                "alt": value.title,
                "width": value.width,
                "height": value.height,
                "renditions": {
                    # "original": generate_image_url(value, "original"),
                },
            }
            rules = getattr(self.meta, "rendition_rules", False)
            if rules:
                for name, rule in rules.items():
                    data["renditions"][name] = generate_image_url(value, rule)
            return data

class RichTextBlock(blocks.RichTextBlock):
    def get_api_representation(self, value, context=None):
        if value:
            return prepare_richtext_for_api(value.source)
        else:
            return ""

