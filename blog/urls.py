from django.views.generic import TemplateView
from django.urls import path, re_path
from . import views

app_name = 'blog'
urlpatterns = [
	path('', views.post_list, name='list'),
    path('create/', views.post_create),
    path('denied/', TemplateView.as_view(template_name='access_denied.html')),
    re_path(r'^(?P<id>\d+)/$', views.post_detail, name='detail'),
    re_path(r'^(?P<id>\d+)/edit/$', views.post_update, name='update'),
    re_path(r'^(?P<id>\d+)/delete/', views.post_delete)

]
