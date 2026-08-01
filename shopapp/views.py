from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from .models import Product
from django.contrib.syndication.views import Feed
from django.views.generic import DetailView
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer, OrderSerializer
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView
import json
from django.http import JsonResponse, Http404
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from .models import User, Order

@login_required
def user_orders_export(request, user_id):
    cache_key = f'user_orders_export_{user_id}'
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return JsonResponse(json.loads(cached_data), safe=False)

    user = User.objects.filter(pk=user_id).first()
    if not user:
        raise Http404("Пользователь не найден")

    orders = Order.objects.filter(user=user).order_by('id')
    serializer = OrderSerializer(orders, many=True)
    data = serializer.data

    cache.set(cache_key, json.dumps(data), 300)

    return JsonResponse(data, safe=False)


@method_decorator(login_required, name='dispatch')
class UserOrdersListView(ListView):
    model = Order
    template_name = 'shopapp/user_orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        self.owner = get_object_or_404(User, pk=user_id)
        return Order.objects.filter(user=self.owner).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shopapp/product_detail.html'
    context_object_name = 'product'



class LatestProductsFeed(Feed):
    title = "Последние товары магазина"
    link = "/products/"
    description = "Обновления ассортимента: новые и актуальные товары."

    def items(self):
        return Product.objects.filter(archived=False).order_by('-id')[:10]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description or f"Товар: {item.name}, цена: {item.price}"

    def item_link(self, item):
        return item.get_absolute_url()



def home(request):
    products = Product.objects.filter(archived=False)
    return render(request, "shopapp/home.html", {"products": products})

def order_list(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
    else:
        orders = Order.objects.none()
    return render(request, "shopapp/order_list.html", {"orders": orders})

class OrderDetailView(PermissionRequiredMixin, DetailView):
    model = Order
    template_name = "shopapp/order_detail.html"
    permission_required = "shopapp.view_order"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrdersExportView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Доступ запрещён")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        orders = (
            Order.objects.select_related("user")
            .prefetch_related("products")
        )
        data = {
            "orders": [
                {
                    "id": order.id,
                    "customer_address": order.customer_address,
                    "notes": order.notes,
                    "user_id": order.user_id,
                    "products": list(order.products.values_list("id", flat=True)),
                }
                for order in orders
            ]
        }
        return JsonResponse(data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "quantity"]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["user", "customer_address"]
    ordering_fields = ["id"]
