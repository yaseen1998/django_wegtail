"""Blog listing and blog detail pages."""
from django import forms
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from rest_framework.fields import Field
from taggit.models import TaggedItemBase
from wagtail.api import APIField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    InlinePanel,
)
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.api.fields import ImageRenditionField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet

from streams import blocks


class BlogListingPage(RoutablePageMixin, Page):
    """Listing page lists all the Blog Detail Pages."""

    template = "blog/blog_listing_page.html"


    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]



    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        context['posts'] = BlogDetailPage.objects.live().public().order_by('-first_published_at')
        context['regular_contaxt_var'] = 'Hello world!'
        context['link'] = self.reverse_subpage(name='latest_posts')
        return context

    @route(r'^latest/$',name='latest_posts')
    def latest_blog_contetnt(self, request, *args, **kwargs):
        """Listing page lists all the Blog Detail Pages."""
        context = self.get_context(request, *args, **kwargs)
        context['posts'] = BlogDetailPage.objects.live().public().order_by('-first_published_at')[:1]
        
        context['name'] = " kalob tertliez"
        context['website'] = 'https://www.google.com'
        return render(request, 'blog/latest_page.html', context)


    def get_sitemap_urls(self,request):
        sitemap = super().get_sitemap_urls(request)
        sitemap.append({
            "location": self.full_url+self.reverse_subpage(name='latest_posts'),
            "lastmod": (self.first_published_at or self.latest_revision_created_at),
            "priority": "0.5"
        })
        return sitemap


class BlogDetailPage(Page):
    """Parental blog detail page."""


    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
    )
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )


    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichtextBlock()),
            ("simple_richtext", blocks.SimpleRichtextBlock()),
            ("cards", blocks.CardBlock()),
            ("cta", blocks.CTABlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        ImageChooserPanel("banner_image"),
        StreamFieldPanel("content"),
    ]






  