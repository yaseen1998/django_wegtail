from django.db import models

from wagtail.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel,PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
class HomePage(Page):
    templates = "home/home_page.html"
    # max_count = 1 # number of child 

    banner_title = models.CharField(max_length=100,blank=False,null=True)
    banner_subtitl = RichTextField(features=['bold','italic']) 
    banner_image = models.ForeignKey (
        "wagtailimages.Image",
        null = True,
        blank = False,
        on_delete = models.SET_NULL,
        related_name = "home_page_banner_image"
    )
    bannerr_cta = models.ForeignKey(
        'wagtailcore.Page',
        null = True,    
        blank = True,   
        on_delete = models.SET_NULL,
        related_name = "home_page_banner_cta"
    )
    content_panels = Page.content_panels + [
        FieldPanel("banner_title"),
        FieldPanel("banner_subtitl"),
        ImageChooserPanel("banner_image"),
        PageChooserPanel("bannerr_cta"),

    ]


    def something(self):
        return self.banner_title

    class Meta : 
        verbose_name = "hellow world"
        verbose_name_plural = "hello worlds "