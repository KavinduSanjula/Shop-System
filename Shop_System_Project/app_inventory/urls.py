from django.urls import path
from .views import index, inventory, inventory_search, update_item, delete_item, sale, delete_sale, update_sale, sale_search

urlpatterns = [
    path('',index, name='index'),
    path('inventory',inventory ,name='inventory'),
    path('search_inventory',inventory_search, name='search-inventory'),
    path('update-item',update_item, name='update-item'),
    path('delete-item',delete_item, name='delete-item'),

    path('sales',sale, name='sale'),
    path('search-sales',sale_search, name='search-sales'),
    path('update-sale',update_sale, name='update-sale'),
    path('delete-sale',delete_sale, name='delete-sale'),
]