from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from django.utils.safestring import mark_safe
from django.conf import settings
from django.db.models import Q
from django.db.models.functions import Length
import json, markdown, bleach

# Create your views here.

from .models import MusicRelease, Post, Tag, Comment, Extra
from .forms import CommentForm, PostForm


def queryRecentPosts(
    tags,
    count="all",
    sort="newest",
):
    orderby = "{0}timestamp".format("-" if sort == "newest" else "")
    if sort == "popular":
        orderby = "hit_count_generic__-hits"

    queryset = Post.objects.order_by(orderby).filter(public__exact=True)
    if len(tags) > 0:
        queryset = queryset.filter(tags__slug__in=tags)
    if count == "all":
        return queryset
    else:
        return queryset[:count]

def queryRecentMusicReleases(
    count="all",
    sort="newest",
):
    orderby = "{0}timestamp".format("-" if sort == "newest" else "")

    queryset = MusicRelease.objects.order_by(orderby).prefetch_related('links').filter(public__exact=True)
    if count == "all":
        return queryset
    else:
        return queryset[:count]


def getRelatedPosts(post):
    qs = (
        Post.objects.filter(
            Q(tags__in=post.tags.all()) & ~Q(pk=post.pk) & Q(public__exact=True)
        )
        .distinct()
        .only("title")
    )
    if len(qs) == 0:
        return Post.objects.filter(Q(public__exact=True) & ~Q(pk=post.pk))
    else:
        return qs


def getAllTags():
    return Tag.objects.all().order_by(Length("title").desc())


def homepage(request):
    queryset = queryRecentPosts([], 4)
    music_releases = queryRecentMusicReleases(5)

    # Create combined list for mobile view
    combined_items = []

    # Add blog posts with type indicator
    for post in queryset:
        combined_items.append({
            'type': 'blog',
            'item': post,
            'timestamp': post.timestamp
        })

    # Add music releases with type indicator
    for release in music_releases:
        combined_items.append({
            'type': 'music',
            'item': release,
            'timestamp': release.timestamp
        })

    # Sort combined list by timestamp (newest first)
    combined_items.sort(key=lambda x: x['timestamp'], reverse=True)

    return render(request, "home.html", {
        "post_list": queryset,
        "music_releases": music_releases,
        "combined_items": combined_items
    })


def music_list(request):
    music_releases = queryRecentMusicReleases()
    return render(request, "music.html", {"music_releases": music_releases})


def post_create(request):
    if not request.user.is_staff:
        return redirect("/blog/denied/")
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid:
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
    whitelist_tags = markdownify_settings.get(
        "WHITELIST_TAGS", bleach.sanitizer.ALLOWED_TAGS
    )
    whitelist_attrs = markdownify_settings.get(
        "WHITELIST_ATTRS", bleach.sanitizer.ALLOWED_ATTRIBUTES
    )
    whitelist_styles = markdownify_settings.get(
        "WHITELIST_STYLES", bleach.sanitizer.ALLOWED_STYLES
    )
    whitelist_protocols = markdownify_settings.get(
        "WHITELIST_PROTOCOLS", bleach.sanitizer.ALLOWED_PROTOCOLS
    )
    cleaner = bleach.Cleaner(
        tags=whitelist_tags,
        attributes=whitelist_attrs,
        styles=whitelist_styles,
        protocols=whitelist_protocols,
        strip=True,
    )

    html = cleaner.clean(md)
    return mark_safe(html)


def post_detail(request, id):
    # Get instance
    instance = get_object_or_404(Post, id=id)
    if not instance.public and not request.user.is_staff:
        return redirect("/blog/denied/")

    # Get associated hitcount
    hit_count = HitCount.objects.get_for_object(instance)
    # Increment hitcount
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    # userMostRecentComment = request.user.getMostRecentComment()

    # Comments
    if request.method == "POST" and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = instance
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(reverse("blog:detail", args=[instance.id]))
    else:
        comment_form = CommentForm()

    context = {
        "title": instance.title,
        "instance": instance,
        "related": getRelatedPosts(instance),
        "changeUrl": "/admin/blog/post/{0}/change/".format(id),
        "comments": instance.comments.all(),
        "comment_form": comment_form,
    }

    if instance.isMarkdownContent:
        markdownify_settings = settings.MARKDOWNIFY["default"]
        extensions = markdownify_settings.get("MARKDOWN_EXTENSIONS", [])
        md = markdown.Markdown(extensions=extensions)
        context["content"] = bleachMarkdown(
            md.convert(instance.content), markdownify_settings
        )
        if "<li>" in md.toc:
            context["has_toc_entries"] = True
        else:
            context["has_toc_entries"] = False
        context["toc"] = md.toc

    return render(request, "post_detail.html", context)


def post_list(request):
    order = request.GET.get("sortBy", "newest")
    tags = request.GET.getlist("tag", [])
    queryset_list = queryRecentPosts(
        tags,
        "all",
        order,
    )
    paginator = Paginator(queryset_list, 10)  # Show 10 Posts per page
    page_request_var = "page"
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
    if not request.user.is_staff:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
        return redirect("/blog/denied/")

    instance = get_object_or_404(Post, id=id)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None, instance=instance)
        try:
            if form.is_valid():
                updated_instance = form.save(commit=False)
                updated_instance.save()

                if is_ajax:
                    # Return JSON response for AJAX requests
                    return JsonResponse({
                        'success': True,
                        'title': updated_instance.title,
                        'content': updated_instance.content,
                        'image_url': updated_instance.image.url if updated_instance.image else None,
                        'public': updated_instance.public,
                        'isMarkdownContent': updated_instance.isMarkdownContent
                    })
                else:
                    messages.success(request, "Item saved")
                    return HttpResponseRedirect(instance.get_absolute_url())
            else:
                if is_ajax:
                    # Return validation errors as JSON
                    return JsonResponse({
                        'success': False,
                        'errors': {field: errors for field, errors in form.errors.items()}
                    }, status=400)
                else:
                    messages.error(request, "Form validation failed")
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=500)
            else:
                messages.warning(
                    request, "Your post was not saved due to an error: {}".format(e)
                )
    else:
        form = PostForm(instance=instance)

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }

    return render(request, "post_form.html", context)


def post_delete(request, id=None):
    if not request.user.is_staff:
        return redirect("/blog/denied/")
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect("blog:list")


def favorites(request):
    results = Extra.objects.filter(public=True).order_by("-timestamp")
    # split = (len(results) // 2) + len(results) % 2
    context = {
        "queryset1": results,
        # "queryset2": results[split:],
    }
    return render(request, "extras.html", context)


def comment_delete(request, id=None):
    if request.method == "DELETE":
        comment = get_object_or_404(Comment, id=id)
        print(request.user)
        if request.user == comment.user or request.user.is_staff:
            comment.delete()
            return HttpResponse(status=204)
    return HttpResponse(status=403)
