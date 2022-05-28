from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel,StreamFieldPanel
from wagtail.core.fields import StreamField
from streams.blocks import *
# Create your models here.
class FlexPage(Page):
    template = "flex/flex_page.html"
    content = StreamField([
        ("title_and_text", TitleAndTextBlock()),
    ],
    null=True,blank=True)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        StreamFieldPanel("content"),
    ]

    class Meta :
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"
