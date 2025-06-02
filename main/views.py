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
# Create your views here.

def auth(request):
    login_form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request,f'привет {request.user}')
                return redirect('main')
    context = {
        'title': 'Авторизация',
        'login_form': login_form,
    }
    return render(request,'auth.html', context)

@login_required
def exit(request):
    logout(request)
    return redirect('auth')

@login_required(login_url="/")
def main(request):
     object_list = Product.objects.all()
     groups = CupGroup.objects.all()
     context = {
        'title':'основная',
        'object_list':object_list,
        'groups': groups,
     }
     return render(request,'main.html', context)

def create_order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_name')
        product = Product.objects.get(id=product_id)
        quantity = request.POST.get('quantity')
        Order.objects.create(product=product, quantity=quantity, user=request.user)
        return JsonResponse({'status': 'success', 'product': product.name})
    return JsonResponse({'status': 'error'}, status=400)

def report(request):
    today = timezone.localtime(timezone.now()).date()
    orders = Order.objects.filter(created_at__date=today)
    paginator = Paginator(orders, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    total_revenue = orders.aggregate(total=Sum(F('quantity') * F('product__price')))['total'] or 0
    context = {
        'title':'отчет',
        'page_obj':page_obj,
        'total_revenue':total_revenue,
     }
    return render(request,'report.html', context)
