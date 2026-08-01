from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from .models import Order, Product


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser', password='qwerty')
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        self.client.force_login(self.user)
        self.product = Product.objects.create(
            name='Хлеб',
            description='',
            price=50,
            quantity=5,
            created_by=self.user,
        )
        self.order = Order.objects.create(
            user=self.user,
            customer_address='ул. Ленина, 10',
            notes='SALE10',
        )
        self.order.products.add(self.product)

    def tearDown(self):
        self.order.delete()
        self.product.delete()

    def test_order_details(self):
        response = self.client.get(reverse('shopapp:order_detail', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.customer_address)
        self.assertContains(response, self.order.notes)
        self.assertEqual(response.context['object'].pk, self.order.pk)


class OrdersExportTestCase(TestCase):
    fixtures = ['users.json', 'products.json', 'orders.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='staffuser', password='qwerty', is_staff=True)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        self.client.force_login(self.user)

    def test_orders_export(self):
        response = self.client.get(reverse('shopapp:orders_export'))
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn('orders', data)

        expected = [
            {
                'id': order.id,
                'customer_address': order.customer_address,
                'notes': order.notes,
                'user_id': order.user_id,
                'products': list(order.products.values_list('id', flat=True)),
            }
            for order in Order.objects.select_related('user').prefetch_related('products')
        ]
        self.assertEqual(data['orders'], expected)