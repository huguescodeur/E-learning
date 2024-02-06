"""
URL configuration for elearning project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from . import views
from account.views import connexion_view
from account.views import inscription_view
from account.views import logout_view
from django.conf import settings
from django.conf.urls.static import static
from videos.views import formations_view
from videos.views import playslist_formations_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name="accueil"),
    path('tutoriels/', views.tutoriels_view, name="tutoriels"),
    path('formations/', formations_view, name="formations"),
    path('formations/playlist', playslist_formations_view,
         name="mes_formations"),
    path('blog/', views.blog_view, name="blog"),
    path('contact/', views.contact_view, name="contact"),
    path('connexion/', connexion_view, name="connexion"),
    path('inscription/', inscription_view, name="inscription"),
    path('logout/', logout_view, name='logout'),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
