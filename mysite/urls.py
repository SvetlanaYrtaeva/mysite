from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from shopapp.sitemaps import ShopSitemap

sitemaps = {
    "shop": ShopSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("auth/", include("myauth.urls")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("", include("shopapp.urls")),
    path("blog/", include("blogapp.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
