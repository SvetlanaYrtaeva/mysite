from django import forms
from .models import Product, Order


class ImportOrdersForm(forms.Form):
    file = forms.FileField()


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'products', 'customer_address', 'notes']