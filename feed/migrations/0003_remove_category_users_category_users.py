# Generated by Django 4.1.3 on 2022-11-23 07:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0002_rename_category_feed_categories_alter_category_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='users',
        ),
        migrations.AddField(
            model_name='category',
            name='users',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]