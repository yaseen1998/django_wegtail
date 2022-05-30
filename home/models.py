from curses import panel
from django.db import models

from wagtail.models import Page
from streams.blocks import *
from wagtail.core.fields import RichTextField,StreamField
from wagtail.admin.edit_handlers import FieldPanel,PageChooserPanel,StreamFieldPanel,InlinePanel,MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.core.models import Orderable
from modelcluster.fields import ParentalKey
from streams import blocks


class HomePAgeCourseImage(Orderable):
    page = ParentalKey('home.HomePage', related_name='carousel_images')
    carousel_image = models.ForeignKey (
        "wagtailimages.Image",
        null = True,
        blank = False,
        on_delete = models.SET_NULL,
        related_name = "+"
    )
    
    panels = [
        ImageChooserPanel('carousel_image')
        ]

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
        MultiFieldPanel([
             FieldPanel("banner_title"),
        FieldPanel("banner_subtitl"),
        ImageChooserPanel("banner_image"),
        PageChooserPanel("bannerr_cta"),
        ],heading="Home Page Banner"),
       MultiFieldPanel([
        InlinePanel("carousel_images",max_num=4,min_num=1,label="image"),
        ],heading="Carousel Images"),
        StreamFieldPanel("content"),
        

    ]
    content = StreamField([
        ('cta', CTABlock()),    
    ],
    null=True,blank=True)


    def something(self):
        return self.banner_title

    class Meta : 
        verbose_name = "hellow world"
        verbose_name_plural = "hello worlds "