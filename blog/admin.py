from django.contrib import admin

# Register your models here.
from .models import Post

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "public", "isMarkdownContent", "timestamp", "updated"]
	list_filter = ["updated", "public", "isMarkdownContent", "timestamp"]
	search_fields = ["title", "content"]
	class Meta:
		model = Post

admin.site.register(Post, PostModelAdmin)