from django.contrib import admin

# Register your models here.
from .models import LinktreeItem, MusicRelease, MusicReleaseLink, Post, Tag, Comment, Extra

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "public", "isMarkdownContent", "timestamp", "updated"]
	list_filter = ["updated", "public", "isMarkdownContent", "timestamp"]
	search_fields = ["title", "content"]
	prepopulated_fields = {"slug": ("title",)}
	class Meta:
		model = Post
class TagModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class CommentModelAdmin(admin.ModelAdmin):
	list_display = ["__str__", "created", "updated"]
	list_filter = ["updated", "created"]
	search_fields = ["content"]
	class Meta:
		model = Comment

class MusicReleaseModelAdmin(admin.ModelAdmin):
    list_display = ["__str__", "public", "timestamp", "updated"]
    list_filter = ["updated", "public", "timestamp"]
    search_fields = ["title", "artist"]
    class Meta:
        model = MusicRelease

class MusicReleaseLinkModelAdmin(admin.ModelAdmin):
	list_display = ["__str__", "platform", "link"]
	class Meta:
		model = MusicReleaseLink

admin.site.register(Tag, TagModelAdmin)
admin.site.register(Post, PostModelAdmin)
admin.site.register(Extra)
admin.site.register(Comment, CommentModelAdmin)
admin.site.register(MusicRelease, MusicReleaseModelAdmin)
admin.site.register(MusicReleaseLink, MusicReleaseLinkModelAdmin)
admin.site.register(LinktreeItem)