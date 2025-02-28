from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Product, Category
from shop.forms import ProductForm

def index(request, category_id=None):
    categories = Category.objects.all()
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all().order_by('-updated_at')
    return render(request, 'shop/home.html', {'products': products, 'categories': categories})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/detail.html', {'product': product})

@login_required(login_url='/admin/')
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'shop/add-product.html', {'form': form})

@login_required(login_url='/admin/')
def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('product_detail', product_id=product.id)
    return render(request, 'shop/product_update.html', {'form': form, 'product': product})

@login_required(login_url='/admin/')
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('index')
    return render(request, 'shop/product_confirm_delete.html', {'product': product})

