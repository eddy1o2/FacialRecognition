"""FacialDetection URL Configuration

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
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404, handler500

from blogs import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^blogs/$', views.PostListView.as_view(), name='blogs'),
    url(r'^blogs/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='post'),
    url(r'^about/$', views.about, name='about'),
    url(r'^streaming/$', views.detected_face, name='streaming'),
    url(r'^video_feed/$', views.video_feed, name='video-feed'),
    url(r'^register/$', views.register, name='register'),
    url(r'^signin/$', auth_views.login, {'template_name': 'login.html'}, name='signin'),
    url(r'^signout/$', auth_views.logout, {'next_page': '/'}, name='signout'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^blogs/new/$', views.new_post, name='new_post'),
    url(r'^data/$', views.get_data, name='get_data'),
    url(r'^resource/$', views.resource, name='resource'),
    url(r'^save_img/$', views.save_img, name='save_img'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'views.error'
handler500 = 'views.error'
