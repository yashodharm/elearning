# Generated by Django 3.0.5 on 2020-05-05 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_auto_20200505_1215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='purchased',
        ),
    ]
