

from django.shortcuts import render,get_object_or_404
from store . models import Product
from category . models import category

from carts.views import _cart_id
from carts.models import CartItem,Cart

from django.db.models import Q


# Create your views here.




def store(request,category_slug = None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(category,slug= category_slug)
        products = Product.objects.filter(category =categories,is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True)

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    except:
        cart_items=None

    # cart       = Cart.objects.get(cart_id=_cart_id(request))   # cart slide
    # cart_items = CartItem.objects.filter(cart=cart, is_active=True)


    context  = {
        'products': products,
        # 'cart_items' : cart_items,
        'cart_items':cart_items,
    
    }
    return render(request, 'store/product.html', context)


def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id= _cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e 
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    except:
        cart_items=None
    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        'cart_items':cart_items,
    }
    return render(request,'store/product_detail.html',context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(describtion__icontains=keyword) | Q(product_name__icontains=keyword))
    context = {
        'products' : products,
    }
    return render(request, 'store/product.html',context)