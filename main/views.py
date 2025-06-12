from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Order, Product, CupGroup
from .forms import LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from datetime import datetime
# Create your views here.

def auth(request):
    login_form = LoginForm(data=request.POST or None)
    if request.user.is_authenticated:
        return redirect('main/no_alco')
    if request.method == 'POST':
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request,f'👋 {request.user}')
                return redirect('main/no_alco')
    context = {
        'title': 'Авторизация',
        'login_form': login_form,
    }
    return render(request,'auth.html', context)

@login_required
def exit(request):
    messages.info(request,f'👋 {request.user}')
    logout(request)
    return redirect('auth')

@login_required(login_url="/")
def main(request, room):
     groups = CupGroup.objects.filter(room=room)
     if request.method == 'POST':
        data = request.POST.copy()
        csrf_token = data.pop('csrfmiddlewaretoken', None)
        if data:
            quantitys = data.getlist('quantity')
            product_ids = data.getlist('product_id')
            products = Product.objects.filter(id__in=product_ids)
            products_dict = {p.id: p for p in products}
            orders_to_create = []
            for quantity, product_id in zip(quantitys,product_ids):
                product = products_dict[int(product_id)]
                order = Order(
                    product=product,
                    quantity=int(quantity),
                    user=request.user
                )
                orders_to_create.append(order)
            Order.objects.bulk_create(orders_to_create)
            messages.info(request,'заказ оформлен')
        else:
            messages.info(request,'зачем отправлять пустой заказ')
        return redirect(request.META.get('HTTP_REFERER'))
     context = {
        'title':'основная',
        'groups': groups,
     }
     return render(request,'main.html', context)

def create_order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_name')
        product = Product.objects.get(id=product_id)
        quantity = request.POST.get('quantity')
        # 
        return JsonResponse({'status': 'success', 'product': {
            'name':product.name,
            'size':product.size.name,
            'id':product.id,
            'price':product.price,
        }})
    return JsonResponse({'status': 'error'}, status=400)

def report(request):
    date_str = request.GET.get('date')
    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date = datetime.now()
    orders = Order.objects.filter(created_at__date=date)
    product_quantities = (
                            orders.values('product__name','product__size__name','product__group__name')  # Группируем по полю 'product'
                            .annotate(
                                total_quantity=Sum('quantity'),
                                total_revenue=Sum(F('quantity') * F('product__price'))
                                )  # Суммируем количество
                            
                            .order_by('product__group__name','-total_quantity')
                        )
    size_quantities = (
                            orders.values('product__group__name','product__size__name')  # Группируем по полю 'product'
                            .annotate(
                                total_quantity=Sum('quantity'),
                                total_revenue=Sum(F('quantity') * F('product__price'))
                                )  # Суммируем количество
                            
                            .order_by('product__group__name','-total_quantity')
                        )
    paginator = Paginator(orders, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    total_revenue = orders.aggregate(total=Sum(F('quantity') * F('product__price')))['total'] or 0
    context = {
        'title':'отчет',
        'page_obj': page_obj,
        'total_revenue': total_revenue,
        'product_quantities': product_quantities,
        'size_quantities': size_quantities,
        'date': date,
     }
    return render(request,'report.html', context)
