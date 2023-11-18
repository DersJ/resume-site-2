from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation

from hitcount.models import HitCount

from users.models import User


# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500, blank=True)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=200)
    displayPath = models.CharField(max_length=40, default="")
    subtitle = models.CharField(max_length=512, blank=True)
    slug = models.SlugField(unique=True)
    image = models.FileField(null=True, blank=True)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    public = models.BooleanField(default=False)
    isMarkdownContent = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)
    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field="object_pk",
        related_query_name="hit_count_generic_relation",
    )

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"id": self.id})

    class Meta:
        ordering = ["-timestamp", "-updated"]


class Extra(models.Model):
    title = models.CharField(max_length=400)
    description = models.TextField(blank=True, default="")
    author = models.CharField(blank=True, max_length=100)
    link = models.URLField(blank=True, default="")
    public = models.BooleanField(default=True)
    ARTICLE = "article"
    BOOK = "book"
    MUSIC = "music"
    VIDEO = "video"
    PODCAST = "podcast"
    TEXT = "text"
    MEME = "meme"
    SITE = "site"
    CONTENT_TYPE_CHOICES = [
        (ARTICLE, "article"),
        (BOOK, "book"),
        (MUSIC, "music"),
        (VIDEO, "video"),
        (PODCAST, "podcast"),
        (TEXT, "text"),
        (MEME, "meme"),
        (SITE, "site"),
    ]
    contentType = models.CharField(
        max_length=10,
        choices=CONTENT_TYPE_CHOICES,
        default=TEXT,
    )
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    score = models.IntegerField(default=0)

    class Meta:
        ordering = ("-score", "-created")

    def __str__(self):
        return "Comment by {} on {}".format(self.user, self.post)


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)
