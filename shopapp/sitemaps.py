from django.contrib.sitemaps import Sitemap
from .models import Product

class ShopSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Product.objects.all().order_by('-id')

    def location(self, obj):
        return obj.get_absolute_url()

