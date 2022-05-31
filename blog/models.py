from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel,StreamFieldPanel
from wagtail.core.fields import StreamField
from streams.blocks import *
from wagtail.images.edit_handlers import ImageChooserPanel

class BlogListingPage(Page):
    template = "blog/blog_listing_page.html"
    coustome_title = models.CharField(max_length=100, blank=False, null=False,help_text="Enter a title for the page")
    content_panels = Page.content_panels + [
        FieldPanel("coustome_title"),

    ]
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['posts'] = BlogDetailPage.objects.live().public()
        return context
   

class BlogDetailPage(Page):
    template = "blog/blog_detail_page.html"
    coustome_title = models.CharField(max_length=100, blank=False, null=False,help_text="Enter a title for the page")
    blog_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content = StreamField([
        ("title_and_text", TitleAndTextBlock()),
        ("richtext", RichtextBlock()),
        ("simple_richtext", SimpleRichtextBlock()),
        ("cards", CardBlock()),
        ('cta', CTABlock()),
        
    ],
    null=True,blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("coustome_title"),
        ImageChooserPanel("blog_image"),
        StreamFieldPanel("content"),
    ]