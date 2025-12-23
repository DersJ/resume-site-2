from django.contrib import admin

# Register your models here.
from .models import LinktreeItem, MusicRelease, MusicReleaseLink, Post, Tag, Comment, Extra

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "public", "isMarkdownContent", "timestamp", "updated"]
	list_filter = ["updated", "public", "isMarkdownContent", "timestamp"]
	search_fields = ["title", "content"]
	prepopulated_fields = {"slug": ("title",)}
	class Meta:
		model = Post
@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
	list_display = ["__str__", "created", "updated"]
	list_filter = ["updated", "created"]
	search_fields = ["content"]
	class Meta:
		model = Comment

@admin.register(MusicRelease)
class MusicReleaseModelAdmin(admin.ModelAdmin):
    list_display = ["__str__", "public", "timestamp", "updated"]
    list_filter = ["updated", "public", "timestamp"]
    search_fields = ["title", "artist"]
    class Meta:
        model = MusicRelease

@admin.register(MusicReleaseLink)
class MusicReleaseLinkModelAdmin(admin.ModelAdmin):
	list_display = ["__str__", "platform", "link"]
	class Meta:
		model = MusicReleaseLink

admin.site.register(Extra)
admin.site.register(LinktreeItem)