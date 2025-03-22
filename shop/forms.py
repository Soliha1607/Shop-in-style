from django import forms
from phonenumber_field.formfields import PhoneNumberField

from shop.models import Product, Comment, Orders


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('product',)


class OrderModelForm(forms.ModelForm):
    phone = PhoneNumberField(region='UZ')

    class Meta:
        model = Orders
        exclude = ('product',)