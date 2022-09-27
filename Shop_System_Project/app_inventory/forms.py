from django.forms import ModelForm
from .models import Item, Sale

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['item_name','price','qty']

class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = ['customer_name','item','date','qty','value']