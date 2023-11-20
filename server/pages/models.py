from django.db import models
from django.utils.translation import gettext_lazy as _
from . import blocks
from wagtail_headless_preview.models import HeadlessMixin
from wagtailmenus.models import MenuPage
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
)
from wagtail.api.conf import APIField
from wagtail.images import get_image_model_string
from .fields import ImageRenditionField
from wagtail.fields import RichTextField, StreamField

# Create your models here.


"""
.##.....##.########.##....##.##.....##
.###...###.##.......###...##.##.....##
.####.####.##.......####..##.##.....##
.##.###.##.######...##.##.##.##.....##
.##.....##.##.......##..####.##.....##
.##.....##.##.......##...###.##.....##
.##.....##.########.##....##..#######.
"""
IMAGE_MODEL = get_image_model_string()

class BasePage(HeadlessMixin, MenuPage):
   
    opengraph_image = models.ForeignKey(
        IMAGE_MODEL,
        verbose_name=_("OpenGraph Image"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    additional_json_ld = models.JSONField(
        null=True,
        blank=True,
    )

    promote_panels = MenuPage.promote_panels + [
        FieldPanel("opengraph_image"),
        FieldPanel("additional_json_ld"),
    ]
    api_fields = [
        APIField("last_published_at"),
        APIField("additional_json_ld"),
        APIField("opengraph_image", serializer=ImageRenditionField({
            'facebook': "fill-600x315-c0",
            'twitter': "fill-300x157-c0"
        }))
    ]
    def get_template(self, request, *args, **kwargs):
        return "pages/main_page.html"


"""
.##.....##..#######..##.....##.########
.##.....##.##.....##.###...###.##......
.##.....##.##.....##.####.####.##......
.#########.##.....##.##.###.##.######..
.##.....##.##.....##.##.....##.##......
.##.....##.##.....##.##.....##.##......
.##.....##..#######..##.....##.########
"""
class HomePage(BasePage):
    body = StreamField([
        ("only_text", blocks.TextBlock()),
        ("image_and_text", blocks.ImageAndText()),
    ], blank=True, null=True,use_json_field=True)

    content_panels = BasePage.content_panels + [
        # StreamFieldPanel('header'),
        FieldPanel("body")
    ]

    api_fields = BasePage.api_fields + [
        # APIField('header'),
        APIField("body")
    ]

    subpage_types = ["pages.BasicPage",]

    
"""
.########.....###.....######..####..######.
.##.....##...##.##...##....##..##..##....##
.##.....##..##...##..##........##..##......
.########..##.....##..######...##..##......
.##.....##.#########.......##..##..##......
.##.....##.##.....##.##....##..##..##....##
.########..##.....##..######..####..######.
"""
class BasicPage(BasePage):

    body = StreamField(
        [
            ("only_text", blocks.TextBlock()),
            ("image_and_text", blocks.ImageAndText()),
            ("focus_Banner", blocks.FocusBanner()),
              
        ],blank=True, null=True,use_json_field=True,
    )

    parent_page_types = [
        "pages.HomePage",
        "pages.BasicPage",
    ]
    subpage_types = [
        "pages.BasicPage",
    ]

    content_panels = BasePage.content_panels + [
        FieldPanel("body"),
    ]

    api_fields = BasePage.api_fields + [
        APIField("body"),
    ]


    

