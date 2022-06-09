# Generated by Django 4.0.4 on 2022-06-09 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('blog', '0005_alter_blogcategory_options_blogdetailpage_categories'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticalBlogPage',
            fields=[
                ('blogdetailpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.blogdetailpage')),
                ('subtitile', models.CharField(blank=True, max_length=100, null=True)),
                ('intro_image', models.ForeignKey(blank=True, help_text='This image will be used to represent the page in the 1400x1400px image.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name': 'Blog Post',
                'verbose_name_plural': 'Blog Posts',
            },
            bases=('blog.blogdetailpage',),
        ),
    ]
