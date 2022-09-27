from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator

from .models import Item, Sale
from .forms import ItemForm, SaleForm


# Create your views here.

def index(request):
    return render(request,'index.html')


def inventory(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory')
        else:
            return HttpResponse('form is not valid')

    items = Item.objects.all().order_by('-id')
    return inventory_render(request, items)
    

def inventory_search(request):
    if request.method == "POST":
        item_name = request.POST['item_name']
        items = Item.objects.filter(item_name__icontains=item_name)
        return inventory_render(request, items)
    else:
        items = Item.objects.all()
        return inventory_render(request, items)


#inventory render common function
def inventory_render(request,items):
    paginator = Paginator(items,10)

    if request.method == 'GET' and request.GET.get('page',None):
        page = request.GET['page']
    else:
        page = 1

    recodes = paginator.get_page(page)
    return render(request,'inventory.html',{'recodes':recodes})


def update_item(request):
    if request.method == 'POST':
        id = request.POST['id']
        item = Item.objects.get(pk=int(id))
        form = ItemForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            return JsonResponse({'id':id,'item_name':item.item_name,'price':item.price, 'qty':item.qty})
        else:
            return HttpResponse('form is invelid')
    else:
        id = request.GET['id']
        item = Item.objects.get(pk=int(id))
        return JsonResponse({'id':id,'item_name':item.item_name,'price':item.price, 'qty':item.qty})

def delete_item(request):
    if request.method == 'POST':
        id = int(request.POST['id'])
        emp = Item.objects.get(pk=id)
        emp.delete()
        return JsonResponse({'message':'success'})
    else:
        return HttpResponse('Method not allowed')



def sale(request):
    if request.method == 'POST':

        item_id = request.POST['item-name']
        item = Item.objects.get(pk=int(item_id))

        value = item.price * int(request.POST['qty'])

        form_data = {'customer_name': request.POST['customer_name'], 'item': item,'qty': request.POST['qty'], 'date':request.POST['date'], 'value':value}
        form = SaleForm(form_data)

        #updating item stock
        item.qty -= int(request.POST['qty'])
        item.save()

        if form.is_valid():
            form.save()
            return redirect('sale')
        else:
            return HttpResponse('form is invalid')

    else:
        sales = Sale.objects.all().order_by('-id')
        items = Item.objects.all()

        return sale_render(request, sales, items)



    

def sale_search(request):
    if request.method == 'POST':
        date = request.POST['date']
        sales = Sale.objects.filter(date=date)
        items = Item.objects.all()

        return sale_render(request, sales, items)
    else:
        sales = Sale.objects.all()
        items = Item.objects.all()
        return sale_render(request, sales, items)



def update_sale(request):
    if request.method == 'POST':
        
        id = request.POST['id']

        item = Item.objects.get(pk=int(request.POST['item']))
        sale = Sale.objects.get(pk=int(id))

        form_data = {'customer_name':request.POST['customer_name'], 'item':item, 'qty':request.POST['qty'], 'value':request.POST['value'], 'date':request.POST['date']}        

        #update item stock
        diff = sale.qty - int(form_data['qty'])
        item.qty += diff
        item.save()

        #recalculate value
        value = int(form_data['qty']) * item.price
        form_data['value'] = value

        form = SaleForm(form_data,instance=sale)

        if form.is_valid():
            sale = form.save()
            return JsonResponse({'id':id,'customer_name':sale.customer_name, 'item':item.item_name, 'date':sale.date, 'qty':sale.qty, 'value':sale.value})
        else:
            return HttpResponse('form is invelid')
    else:
        id = request.GET['id']
        sale = Sale.objects.get(pk=int(id))

        return JsonResponse({'id':id,'customer_name':sale.customer_name, 'item':sale.item.item_name, 'date':sale.date, 'qty':sale.qty, 'value':sale.value, 'item_id':sale.item.id})


def delete_sale(request):
    if request.method == 'POST':
        id = int(request.POST['id'])
        sale = Sale.objects.get(pk=id)

        #update item stock
        sale.item.qty += sale.qty
        sale.item.save()

        sale.delete()
        return JsonResponse({'message':'success'})
    else:
        return HttpResponse('Method not allowed')


# sale render common function
def sale_render(request, sales, items):

    total_price = 0
    for sale in sales:
        if sale.value:
            total_price += sale.value

    if request.method == 'GET' and request.GET.get('page',None):
        page = request.GET['page']
    else:
        page = 1

    paginator = Paginator(sales, 10)
    recodes = paginator.get_page(page)
    return render(request,'sell.html',{'recodes':recodes, 'items':items, 'total':total_price})