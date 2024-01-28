from django.contrib import admin

# Register your models here.
from .models import Post, Tag, Comment, Extra

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

admin.site.register(Tag, TagModelAdmin)
admin.site.register(Post, PostModelAdmin)
admin.site.register(Extra)
admin.site.register(Comment, CommentModelAdmin)