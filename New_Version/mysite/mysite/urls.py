from django.contrib import admin
from django.urls import path,include
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static

from blog.sitemaps import PostSitemap


sitemaps = {
    'posts':PostSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/',include('blog.urls',namespace='blog')),
    path('sitemap.xml',sitemap,{'sitemaps':sitemaps},
        name='django.contirb.sitemaps.views.sitemap'),
        
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
