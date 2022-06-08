# Generated by Django 4.0.4 on 2022-06-08 10:19

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blogcategory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogcategory',
            options={'ordering': ['-name'], 'verbose_name': 'Blog Category', 'verbose_name_plural': 'Blog Categories'},
        ),
        migrations.AddField(
            model_name='blogdetailpage',
            name='categories',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='blog.blogcategory'),
        ),
    ]