from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from shop.models import Product, Category, Comment
from shop.forms import ProductForm, CommentForm, OrderForm
from django.db.models import Avg



def index(request, category_id=None):
    search_query = request.GET.get('q', '')
    categories = Category.objects.all()
    filter_query = request.GET.get('filter', '')

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all().order_by('-updated_at')

    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    if filter_query == 'expensive':
        products = products.order_by('-price')

    elif filter_query == 'cheap':
        products = products.order_by('price')

    elif filter_query == 'rating':
        products = products.annotate(rating_avg=Avg('comments__rating')).order_by('-rating_avg')

    return render(request, 'shop/home.html', {'products': products, 'categories': categories})


def product_detail(request, product_id):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.all().annotate(rating_avg=Avg('comments__rating')).filter(
        category=product.category).exclude(id=product.id).order_by('-rating_avg')
    comments = product.comments.all()
    context = {
        'product': product,
        'categories': categories,
        'comments': comments,
        'related_products': related_products
    }
    return render(request, 'shop/detail.html', context)


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
    return render(request, 'shop/product-update.html', {'form': form, 'product': product})


@login_required(login_url='/admin/')
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('index')
    return render(request, 'shop/product-create.html', {'product': product})

def products_of_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/base/base.html', {'category': category, 'products': products})


def comment_list(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = Comment.objects.filter(product=product).order_by('-created_at')
    return render(request, 'shop/detail.html', {'product': product, 'comments': comments})


def comment_view(request, pk):
    product = Product.objects.get(id=pk)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            rating = request.POST.get('rating')
            print(type(rating))
            comment.rating = rating
            comment.product = product
            comment.save()
            return redirect('product_detail', product.id)

    context = {
        'form': form,
        'product': product
    }

    return render(request, 'shop/detail.html', context)


def order_view(request, pk):
    product = Product.objects.get(id=pk)
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        quantity = int(request.POST.get('quantity'))
        if form.is_valid():
            if product.quantity >= quantity:
                order = form.save(commit=False)
                order.product = product
                product.quantity = product.quantity - quantity
                product.save()
                order.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Order successfully created'
                )
                return redirect('product_detail', product.id)
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Something is wrong'
                )
    return render(request, 'shop/detail.html', {'form': form, 'product': product})
