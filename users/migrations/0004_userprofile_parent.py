# Generated by Django 3.0.5 on 2020-05-10 10:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200505_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='parent',
            field=models.ManyToManyField(blank=True, related_name='_userprofile_parent_+', to=settings.AUTH_USER_MODEL),
        ),
    ]