"""resumesite2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path 
from django.views.generic import TemplateView

from blog.views import homepage, favorites
from users.views import profile 
from biking.views import map_view, importRides, activity_data
from .views import nostr


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', profile),
    path('blog/', include('blog.urls', namespace='blog')),
	path('', homepage, name='home'),
    path('about', TemplateView.as_view(template_name='about.html')),
    path('extras/', favorites, name='extras'),
    path('resume/', TemplateView.as_view(template_name="resume.html")),
    path('projects/', TemplateView.as_view(template_name='projects2.html')),
    path('contact/', TemplateView.as_view(template_name='contact.html')),
    path('coursework/', TemplateView.as_view(template_name='coursework.html')),
    path('engl105/', TemplateView.as_view(template_name='engl105/index.html')),
    path('engl105/personal/', TemplateView.as_view(template_name='engl105/personal.html')),
    path('engl105/science/', TemplateView.as_view(template_name='engl105/science.html')),
    path('engl105/conflict/', TemplateView.as_view(template_name='engl105/conflict.html')),
    path('engl105/reflection/', TemplateView.as_view(template_name='engl105/reflection.html')),
    path('biking/import/', importRides, name='importRides'),
    path('biking/data/', activity_data, name='biking_data'),
    path('bike-map/', map_view, name='biking'),
    path('.well-known/nostr.json', nostr, name='nostr_config'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

