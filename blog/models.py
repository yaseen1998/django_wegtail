"""Blog listing and blog detail pages."""
from tabnanny import verbose
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
        # context['posts'] = BlogDetailPage.objects.live().public().order_by('-first_published_at')
        context['regular_contaxt_var'] = 'Hello world!'
        context['link'] = self.reverse_subpage(name='latest_posts')
        context['author'] = BlogAuthor.objects.all()
        context['categories'] = BlogCategory.objects.all()
        all_post = BlogDetailPage.objects.live().public().order_by('-first_published_at')
        paginator = Paginator(all_post, 1)
        page = request.GET.get('page')
        try : 
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        
        context['posts'] = posts
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

    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)

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
        MultiFieldPanel([
            InlinePanel("blog_authors", label="Author",min_num = 1,max_num = 3),
        ], heading="Author(s)"),
        MultiFieldPanel([
            FieldPanel("categories",widget = forms.CheckboxSelectMultiple),
        ], heading="Categories"),
    
    ]




class BlogAuthor(models.Model):
    """Blog author."""

    name = models.CharField(max_length=255)
    website = models.URLField(blank=True,null = True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name = '+'
    )

    panels = [
        MultiFieldPanel([
            FieldPanel("name"),
            ImageChooserPanel('image'),
        ],
        heading = 'Author Info',
        ),
        MultiFieldPanel([
            FieldPanel("website"),
        ],
        heading = 'Author Links',
        )
        
    ]
    class Meta : 
        verbose_name = 'Blog Author'
        verbose_name_plural = 'Blog Authors'
        


    def __str__(self):
        return self.name

register_snippet(BlogAuthor)

  
class BlogAuthorOrderable(Orderable):
    """Blog author orderable."""

    page = ParentalKey(
        "blog.BlogDetailPage",
        related_name="blog_authors",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("author"),
    ]
    
    
    
class BlogCategory(models.Model):
    """Blog category."""

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text="A slug is a short text label, generally used in URLs, "
        )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering=['-name']

register_snippet(BlogCategory)



# first subclass blog post page 
class ArticalBlogPage(BlogDetailPage):
    """A subclass of the Blog Detail Page."""

    template = 'blog/artical_blog_page.html'
    subtitile = models.CharField(max_length=100, blank=True, null=True)
    intro_image = models.ForeignKey("wagtailimages.Image",blank=True,null=True,on_delete=models.SET_NULL
                                    ,related_name="+",help_text = "This image will be used to represent the page in the 1400x1400px image.")
    
    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("subtitile"),
        ImageChooserPanel("banner_image"),
        ImageChooserPanel("intro_image"),
        StreamFieldPanel("content"),
        MultiFieldPanel([
            InlinePanel("blog_authors", label="Author",min_num = 1,max_num = 3),
        ], heading="Author(s)"),
        MultiFieldPanel([
            FieldPanel("categories",widget = forms.CheckboxSelectMultiple),
        ], heading="Categories"),
    
    ]
    
    class Meta:
        verbose_name = "Artical Blog"
        verbose_name_plural = "Artical Blogs"
 
 
 # seocnd subclass page
class VideoBlogPage(BlogDetailPage):
    youtube_video_id = models.CharField(max_length=100, blank=True, null=True)
    
    template = 'blog/video_blog_page.html'
    
    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("youtube_video_id"),
        ImageChooserPanel("banner_image"),
        StreamFieldPanel("content"),
        MultiFieldPanel([
            InlinePanel("blog_authors", label="Author",min_num = 1,max_num = 3),
        ], heading="Author(s)"),
        MultiFieldPanel([
            FieldPanel("categories",widget = forms.CheckboxSelectMultiple),
        ], heading="Categories"),
    
    ]
    

    """
    just BlogDetailpage / BlogDetailPage.objects.live().exact_type(BlogDetailPage)
    every thing except the BlogDetailpage / BlogDetailPage.objects.live().not_exact_type(BlogDetailPage)
    BlogDetailPage.objects.live().exact_type(ArticalBlogPage).specific(defer=False)
    """