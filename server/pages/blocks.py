
from wagtail import blocks
from wagtailutils import blocks as utilblocks
from wagtail.images.blocks import ImageChooserBlock

"""
.########..##........#######...######..##....##..######.
.##.....##.##.......##.....##.##....##.##...##..##....##
.##.....##.##.......##.....##.##.......##..##...##......
.########..##.......##.....##.##.......#####.....######.
.##.....##.##.......##.....##.##.......##..##.........##
.##.....##.##.......##.....##.##....##.##...##..##....##
.########..########..#######...######..##....##..######.
"""
class TextBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    text = utilblocks.RichTextBlock(required=True)

    class Meta:
        icon = "doc-full-inverse"


class ImageAndText(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    text = utilblocks.RichTextBlock(required=False)
    image = ImageChooserBlock(
        required=False,
        help_text="Optimal Dimension : 441x400",
        rendition_rules={
            "original": "fill-441x400-c0|format-webp",
            "original_fallback": "fill-441x400-c0",
        },
    )
    image_alignment = blocks.ChoiceBlock(choices=(
        ('left', 'Left'), ('right', 'Right')), default='right')
    image_margin = blocks.BooleanBlock(required=False, default=False)
    top_padding = blocks.BooleanBlock(required=False, default=True)
    bottom_padding = blocks.BooleanBlock(required=False, default=True)



class FocusBanner(blocks.StructBlock):
    mega_image = utilblocks.ImageChooserBlock(
        required=True,
        help_text="Optimal Dimension : 986x493",
        rendition_rules={
            "original": "fill-986x493-c0|format-webp",
            "original_fallback": "fill-986x493-c0",
        },
    )
    baby_image = utilblocks.ImageChooserBlock(
        required=False,
        help_text="Optimal Dimension : max width 250px",
        rendition_rules={
            "original": "width-250|scale-100|format-webp",
            "original_fallback": "width-250|scale-100",
        },
    )