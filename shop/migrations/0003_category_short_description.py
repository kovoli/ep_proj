# Generated by Django 2.2.4 on 2019-08-10 18:09

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_category_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='short_description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]