from django import forms
from app_shop.models import Product


class VendorProductForm(forms.ModelForm):
    coupon_code = forms.CharField(required=False, widget=forms.TextInput(
        attrs={"placeholder": "if you want to add"}))
    old_price = forms.FloatField(required=False)

    class Meta:
        model = Product
        exclude = ["user", "created"]
