from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):
    help = 'Создание продуктов через get_or_create'

    def handle(self, *args, **options):
        user = User.objects.filter(
            is_active=True
        ).order_by('id').first()

        if user is None:
            self.stdout.write(
                self.style.ERROR(
                    'Нет пользователей. '
                    'Создайте суперпользователя.'
                )
            )
            return

        products_data = [
            {
                'name': 'iPhone 15 Pro',
                'description': (
                    'Смартфон Apple с процессором A17 Pro, '
                    '256GB, Titanium'
                ),
                'price': 150000,
                'quantity': 50,
                'archived': False,
                'created_by': user,
            },
            {
                'name': 'Samsung Galaxy S24',
                'description': (
                    'Флагманский смартфон Samsung '
                    'с AI-функциями, 512GB'
                ),
                'price': 120000,
                'quantity': 75,
                'archived': False,
                'created_by': user,
            },
            {
                'name': 'Sony WH-1000XM5',
                'description': (
                    'Беспроводные наушники '
                    'с подавлением шума'
                ),
                'price': 35000,
                'quantity': 100,
                'archived': False,
                'created_by': user,
            },
        ]

        for data in products_data:
            product, created = Product.objects.get_or_create(
                name=data['name'],
                defaults=data
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Создан продукт: {product.name}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Продукт уже существует: {product.name}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Всего продуктов: {Product.objects.count()}'
            )
        )