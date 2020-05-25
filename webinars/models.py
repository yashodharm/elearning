from __future__ import unicode_literals
import os
from users.models import UserProfile

from django.db import models
from users.models import UserProfile
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.dispatch import receiver

# Create your models here.
class Webinar(models.Model):
    webinar_name = models.CharField(unique=True, max_length=20)
    webinar_created_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(default=None,null=True)
    link = models.URLField(default=None,null=True,blank=True)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE, default=1)
    # students = models.ManyToManyField(UserProfile, related_name='students_to_course')
    students = models.ManyToManyField(UserProfile,through="join", related_name='students_to_webinars')

    for_everybody = models.BooleanField(default=True)
    def __unicode__(self):
        return self.course_name

class join(models.Model):
    user=models.ForeignKey(UserProfile ,on_delete=models.CASCADE)
    webinar=models.ForeignKey(Webinar , on_delete=models.CASCADE)
    

class Session(models.Model):
    session_name = models.CharField(max_length=20)
    session_created_date = models.DateTimeField(auto_now_add=True)
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE, default=1)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.chapter_name

    def get_absolute_url(self):
        return reverse("session", kwargs={"webinar_name": self.webinar.webinar_name,
                                          "slug": self.slug})

    def slug_default(self):
        slug = create_slug(new_slug=self.session_name)
        return slug


def create_slug(instance=None, new_slug=None):
    slug = slugify(instance.session_name)

    if new_slug is not None:
        slug = new_slug

    qs = Session.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()

    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)

    return slug


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_receiver, sender=Session)


class TextBlockW(models.Model):
    lesson = models.TextField()
    text_block_fk = models.ForeignKey(Session,  on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


class YTLinkW(models.Model):
    link = models.URLField(max_length=200)
    yt_link_fk = models.ForeignKey(Session,  on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

class gdlinkW(models.Model):
    link = models.URLField(max_length=200)
    gd_link_fk = models.ForeignKey(Session,  on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


class FileUploadW(models.Model):
    file = models.FileField(null=False, blank=False, default='')
    date_created = models.DateTimeField(auto_now_add=True)
    file_fk = models.ForeignKey(Session,  on_delete=models.CASCADE)


@receiver(models.signals.post_delete, sender=FileUploadW)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
