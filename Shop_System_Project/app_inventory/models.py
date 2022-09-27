from django.db import models

# Create your models here.

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=3,max_digits=15)
    qty = models.IntegerField(null=True)

    def __repr__(self):
        return f"{self.item_name} | {self.price}"

class Sale(models.Model):
    customer_name = models.CharField(max_length=100,null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)
    qty = models.IntegerField()
    value = models.DecimalField(decimal_places=3,max_digits=15, null=True)

    def __repr__(self):
        return f"{self.item} | {self.qty}"