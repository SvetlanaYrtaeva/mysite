from django.core.management.base import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):
    help = "Создание продуктов через get_or_create"

    def handle(self, *args, **options):
        products_data = [
            {
                'name': 'iPhone 15 Pro',
                'description': 'Смартфон Apple с процессором A17 Pro, 256GB, Titanium',
                'price': 150000,
                'quantity': 50,
                'is_available': True
            },
            {
                'name': 'Samsung Galaxy S24',
                'description': 'Флагманский смартфон Samsung с AI-функциями, 512GB',
                'price': 120000,
                'quantity': 75,
                'is_available': True
            },
            {
                'name': 'Sony WH-1000XM5',
                'description': 'Беспроводные наушники с превосходным подавлением шума',
                'price': 35000,
                'quantity': 100,
                'is_available': True
            },
        ]

        for data in products_data:
            product, created = Product.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Создан продукт: {product.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'→ Продукт уже существует: {product.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nВсего продуктов в базе: {Product.objects.count()}')
        )