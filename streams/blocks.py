from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
class TitleAndTextBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Add a title")
    text = blocks.TextBlock(required=True, help_text="Add text")

    class Meta:
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"

class RichtextBlock(blocks.RichTextBlock):
    class Meta:
        template = "streams/richtext_block.html"
        icon = "doc-full"
        label = "Full Richtext"

class SimpleRichtextBlock(blocks.RichTextBlock):
    def __init__(self, required=True, help_text=None, editor='default', features=None, validators=(), **kwargs):
        super().__init__(**kwargs)
        self.features = [
            'bold', 'italic', 'link',
        ]
        
    class Meta:
        template = "streams/simple_richtext_block.html"
        icon = "edit"
        label = "simple Richtext"


class CardBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Add a title")


    cards = blocks.ListBlock(
        blocks.StructBlock([
            ('card_title', blocks.CharBlock(required=True, help_text="Add a title",max_length=100)),
            ('card_text', blocks.TextBlock(required=True,max_length=200, help_text="Add text")),
            ('image',ImageChooserBlock(required=False)),
            ('button_page', blocks.PageChooserBlock(required=False)),
            ('button_url', blocks.URLBlock(required=False, help_text="Button will link to this URL")),
        ]))
    class Meta:
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "Card"

class CTABlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Add a title",max_length=100)
    text = blocks.RichTextBlock(required=True, features=['bold', 'italic'])
    button_page = blocks.PageChooserBlock(required=False)
    button_text = blocks.CharBlock(required=True, max_length=40,default = "Learn More")
    button_url = blocks.URLBlock(required=False, help_text="Button will link to this URL")
    class Meta:
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to Action"
  
  
class LinkStructValue(blocks.StructValue):
    def url(self):
        if self.get('button_page'):
            return self.get('button_page').url
        elif self.get('button_url'):
            return self.get('button_url')
        else:
            return None      
        
class ButtonBlock(blocks.StructBlock):
    button_page = blocks.PageChooserBlock(required=False,help_text="Button will link to this page")
    button_url = blocks.URLBlock(required=False,help_text="Button will link to this URL")
    
    class Meta:
        template = "streams/button_block.html"
        icon = "placeholder"
        label = "button block"
        value_class = LinkStructValue
        
        
