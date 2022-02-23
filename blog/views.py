from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.

from .models import Post
from .forms import PostForm


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


def post_detail(request, id):
	instance = get_object_or_404(Post, id=id)

	context = {
		"title": instance.title,
		"instance": instance,
	}
	return render(request, "post_detail.html", context)


def post_list(request):
	queryset_list = Post.objects.filter(public__exact=True)  #.order_by("-timestamp")

	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
	page_request_var="page"
	page = request.GET.get(page_request_var)
	queryset = paginator.get_page(page)

	context = {
		"object_list": queryset,
		"title": "List",	
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