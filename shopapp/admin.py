from django.contrib import admin
from .models import Product, Order
import csv
from io import TextIOWrapper
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from .forms import ImportOrdersForm


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'archived')
    list_filter = ('archived',)
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    filter_horizontal = ('products',)

    change_list_template = 'shopapp/orders_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'import-csv/',
                self.admin_site.admin_view(self.import_csv_view),
                name='import_orders_csv',
            ),
        ]
        return custom_urls + urls

    def import_csv_view(self, request):
        if request.method == 'POST':
            form = ImportOrdersForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES['file']
                csv_file = TextIOWrapper(file, encoding='utf-8')
                reader = csv.reader(csv_file)

                errors = []
                success_count = 0

                for row_num, row in enumerate(reader, start=1):
                    if not row or len(row) < 4:
                        continue

                    try:
                        user_id = int(row[0])
                        customer_address = row[1]
                        notes = row[2]
                        product_ids_raw = [x.strip() for x in row[3].split(',') if x.strip()]
                        product_ids = [int(x) for x in product_ids_raw]

                        order = Order.objects.create(
                            user_id=user_id,
                            customer_address=customer_address,
                            notes=notes,
                        )

                        products = Product.objects.filter(id__in=product_ids)
                        if products.count() != len(product_ids):
                            missing = set(product_ids) - {p.id for p in products}
                            if missing:
                                errors.append(f"Строка {row_num}: не найдены товары с ID: {missing}")

                        order.products.set(products)
                        success_count += 1

                    except Exception as e:
                        errors.append(f"Строка {row_num}: ошибка — {str(e)}")

                if errors:
                    for err in errors:
                        self.message_user(request, err, level='ERROR')
                else:
                    self.message_user(request, "Импорт успешно завершён!", level='SUCCESS')

                return HttpResponseRedirect('../')

        else:
            form = ImportOrdersForm()

        context = self.admin_site.each_context(request)
        context['form'] = form
        return render(request, 'admin/csv_form.html', context)

