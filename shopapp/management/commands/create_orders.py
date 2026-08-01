from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order, Product


class Command(BaseCommand):
    help = "Создание заказов через get_or_create"

    def handle(self, *args, **options):
        users = User.objects.all()
        if not users:
            self.stdout.write(
                self.style.ERROR('Нет пользователей. Создайте суперпользователя!')
            )
            return

        products = Product.objects.all()
        if not products:
            self.stdout.write(
                self.style.ERROR('Нет продуктов. Выполните create_products сначала!')
            )
            return

        user = users[0]

        orders_data = [
            {
                'customer_address': 'г. Москва, ул. Тверская 1',
                'notes': 'Доставить до 18:00',
                'product_names': ['iPhone 15 Pro', 'Sony WH-1000XM5']
            },
            {
                'customer_address': 'г. Санкт-Петербург, Невский 25',
                'notes': 'Курьеру звонить заранее',
                'product_names': ['Samsung Galaxy S24']
            },
        ]

        for order_data in orders_data:
            order_products = Product.objects.filter(
                name__in=order_data['product_names']
            )

            order, created = Order.objects.get_or_create(
                customer_address=order_data['customer_address'],
                user=user,
                defaults={'notes': order_data['notes']}
            )

            for product in order_products:
                order.products.add(product)

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Создан заказ #{order.id}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'→ Заказ уже существует: #{order.id}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nВсего заказов: {Order.objects.count()}')
        )