from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from django.utils.safestring import mark_safe
from django.conf import settings
from django.db.models import Q
from django.db.models.functions import Length
import json, markdown, bleach
# Create your views here.

from .models import *
from .forms import PostForm

def queryRecentPosts(request, tags, count='all', sort='newest', ):
	orderby = '{0}timestamp'.format('-' if sort == 'newest' else '')
	if (sort == 'popular'):
		orderby = 'hit_count_generic__-hits'

	queryset = Post.objects.order_by(orderby).filter(public__exact=True)
	if len(tags) > 0:
		queryset = queryset.filter(tags__slug__in=tags)
	if count == 'all':
		return queryset
	else:
		return queryset[:count]

def getRelatedPosts(post):
	qs = Post.objects.filter(Q(tags__in=post.tags.all()) & ~Q(pk=post.pk)).distinct().only("title")
	if len(qs) == 0:
		return Post.objects.filter(public__exact=True)
	else:
		return qs


def getAllTags():
	return Tag.objects.all().order_by(Length('title').desc())

def homepage(request):
	queryset = queryRecentPosts(request, [], 3)
	return render(request, "home.html", { "post_list": queryset })

def post_create(request):
	if not request.user.is_authenticated:
		return redirect('/blog/denied/')
	if (request.method == 'POST'):
		form = PostForm(request.POST, request.FILES or None)
		if(form.is_valid):

			instance = form.save(commit=False)
			instance.save()
			messages.success(request, "Successfully Created")
			return HttpResponseRedirect(instance.get_absolute_url())
		else:
			messages.error(request, "Error")
	else:
		form = PostForm()

	context = {
		"form": form,
	}
	return render(request, "post_form.html", context)

def bleachMarkdown(md, markdownify_settings):
	whitelist_tags = markdownify_settings.get('WHITELIST_TAGS', bleach.sanitizer.ALLOWED_TAGS)
	whitelist_attrs = markdownify_settings.get('WHITELIST_ATTRS', bleach.sanitizer.ALLOWED_ATTRIBUTES)
	whitelist_styles = markdownify_settings.get('WHITELIST_STYLES', bleach.sanitizer.ALLOWED_STYLES)
	whitelist_protocols = markdownify_settings.get('WHITELIST_PROTOCOLS', bleach.sanitizer.ALLOWED_PROTOCOLS)
	cleaner = bleach.Cleaner(tags=whitelist_tags,
								attributes=whitelist_attrs,
								styles=whitelist_styles,
								protocols=whitelist_protocols,
								strip=True
								)

	html = cleaner.clean(md)
	return mark_safe(html)

def post_detail(request, id):
	instance = get_object_or_404(Post, id=id)
	hit_count = HitCount.objects.get_for_object(instance)
	hit_count_response = HitCountMixin.hit_count(request, hit_count)
	context = {
		"title": instance.title,
		"instance": instance,
		"related": getRelatedPosts(instance),
		"changeUrl": '/admin/blog/post/{0}/change/'.format(id),
	}
	if instance.isMarkdownContent:
		markdownify_settings = settings.MARKDOWNIFY['default']
		extensions = markdownify_settings.get('MARKDOWN_EXTENSIONS', [])
		md = markdown.Markdown(extensions=extensions)
		context['content'] = bleachMarkdown(md.convert(instance.content), markdownify_settings)
		context['toc'] = md.toc

	return render(request, "post_detail.html", context)


def post_list(request):
	order = request.GET.get('sortBy', 'newest')
	tags = request.GET.getlist('tag', [])
	queryset_list = queryRecentPosts(request, tags, 'all', order, )
	paginator = Paginator(queryset_list, 10) # Show 10 Posts per page
	page_request_var="page"
	page = request.GET.get(page_request_var)
	queryset = paginator.get_page(page)

	context = {
		"object_list": queryset,
		"title": "List",
		"sortBy": order,
		"appliedTags": json.dumps(tags),
		"allTags": getAllTags(),
		"page_request_var": page_request_var,
	}
	return render(request, "post_list.html", context)

def post_update(request, id=None):
	if not request.user.is_authenticated:
		return redirect('/blog/denied/')
	instance = get_object_or_404(Post, id=id)

	if request.method=="POST":
		form = PostForm(request.POST or None, request.FILES or None, instance=instance)
		try:
			if(form.is_valid):
				form.save(commit=False).save()
				messages.success(request, "Item saved")
		except Exception as e:
			messages.warning(request, "Your post was not saved due to an error: {}".format(e))
	else:
		form = PostForm(instance=instance)

	context = {
		"title": instance.title,
		"instance": instance,
		"form": form,
	}

	return render(request, "post_form.html", context)

def post_delete(request, id=None):
	if not request.user.is_authenticated:
		return redirect('/blog/denied/')
	instance = get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request, "Successfully Deleted")
	return redirect("blog:list")

def favorites(request):
	results = Extra.objects.filter(public=True).order_by('title')
	split = (len(results) // 2) + len(results) % 2
	context = {
		"queryset1": results[:split],
		"queryset2": results[split:],
	}
	return render(request, "extras.html", context)
