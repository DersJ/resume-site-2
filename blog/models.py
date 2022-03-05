from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify

# Create your models here.
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

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("blog:detail", kwargs={"id": self.id})
		
	class Meta:
		ordering = ["-timestamp", "-updated"]

def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by('-id')
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug
def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug= create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)