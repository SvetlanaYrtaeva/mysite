from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    home, order_list, OrderDetailView, OrdersExportView,
    ProductViewSet, OrderViewSet, LatestProductsFeed,
    ProductDetailView, UserOrdersListView, user_orders_export,  # <-- добавили эти два
)

app_name = 'shopapp'
router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"orders", OrderViewSet)

urlpatterns = [
    path("", home, name="home"),

    path("product/<int:pk>/", ProductDetailView.as_view(), name='product_detail'),

    path("orders/", order_list, name="order_list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("orders/export/", OrdersExportView.as_view(), name="orders_export"),

    path('users/<int:user_id>/orders/', UserOrdersListView.as_view(), name='user_orders_list'),
    path('users/<int:user_id>/orders/export/', user_orders_export, name='user_orders_export'),

    path("api/", include(router.urls)),
    path('products/latest/feed/', LatestProductsFeed(), name='latest_products_feed'),
]
