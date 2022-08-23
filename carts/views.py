


from django.shortcuts import get_object_or_404, redirect, render
from carts.models import CartItem,Cart

from store.models import Product, Variation
from django.core.exceptions import ObjectDoesNotExist


from django.contrib.auth.decorators import login_required
from coupon . models import Coupon,CouponUsers
# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) #get the product
    # if the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
                 
            for item in request.POST:
                key = item 
                value = request.POST[key]
                

                try:
                    variation = Variation.objects.get(product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value)
                    product_variation.append(variation)
                    
                except:
                    
                    pass
       
        is_cart_item_exists = CartItem.objects.filter(product=product,user=current_user).exists()
        
        if is_cart_item_exists: 
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            # existing_variations -> database
            # current variations -> product_variation
            # item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)


            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                print("aaaaaaaaaaaaaaaa")
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
    # variation
                if len(product_variation) >  0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()


        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user
            )
    # variation

            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            
            cart_item.save()
        return redirect('cart')

# if the user is not authenticated

    else:
        product_variation = []
        if request.method == 'POST':
                  
            for item in request.POST:
                key = item 
                value = request.POST[key]
                

                try:
                    
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                    variation_value__iexact=value)
                    product_variation.append(variation)
                    
                except:
                    pass
                


        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()





        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        
        if is_cart_item_exists: 
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # existing_variations -> database
            # current variations -> product_variation
            # item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)


            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                print("pppppppppppppp")
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1,cart=cart)
    # variation
                if len(product_variation) >  0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()


        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
    # variation

            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            
            cart_item.save()
        return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
   
    product = get_object_or_404(Product, id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id,cart_item_id):
    
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product =product, user=request.user, id= cart_item_id)
        print("000000000bhrtgshrjty0000000000")
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product =product, cart=cart, id= cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request,total=0,quantity=0, cart_items=None):
    
    try:
        tax=0
        grand_total=0
        coupon =0
        couponlist=None
        offernote=""
        
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            if CouponUsers.objects.filter(user=request.user, is_used= False).exists() :
                coupon_user = CouponUsers.objects.get(user=request.user, is_used= False)
                print('----------------------------')
                print(coupon_user)
                coupon = coupon_user.amount 
                print('++++++++++++++++++++++++++++++++++++++')
                print(coupon)
                print(coupon_user.is_used)
            else:
                coupon = 0
                
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            # pass
        
        try:
                    
            for cart_item in cart_items:
                total +=(cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
        except:
            pass
        
        tax = (2 * total/100 )
        grand_total = total + tax - coupon
        if grand_total>=2000:
            couponlist = Coupon.objects.filter( amount=500,is_available=True)
        elif grand_total>=900:
            couponlist = Coupon.objects.filter( amount=100,is_available=True)
        else:
            offernote = "Purchase above ₹ 900 for special offers"
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax' : tax,
        'grand_total' : grand_total,
        'coupon' : coupon,
        'couponlist' : couponlist,
        'offernote' : offernote,
        
    }
    return render(request,'store/cart.html',context)


@login_required(login_url='login')
def checkout(request,total=0,quantity=0, cart_items=None):
    try:
        tax=0
        grand_total=0
        coupon =0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart       = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total +=(cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        
        if CouponUsers.objects.filter(user=request.user, is_used= False).exists() :
            coupon_user = CouponUsers.objects.get(user=request.user, is_used= False)
            print('----------------------------')
            print(coupon_user)
            coupon      = coupon_user.amount 
            # coupon_user.is_used= True
            # coupon_user.save()
            print('*************************')
            print(coupon_user.is_used)
        tax = (2 * total/100 )
        grand_total = total + tax - coupon

    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax' : tax,
        'grand_total' : grand_total,
        'coupon' : coupon,
        
    }
    return render(request,'store/checkout.html', context)

@login_required(login_url='login')
def add_coupon(request):

    if request.method == 'POST':
        code = request.POST['codew']

        if Coupon.objects.filter(coupon_code=code, is_available=True).exists() and  CouponUsers.objects.filter(user= request.user).exists() == False :
            print('poiuytr')
            coupon_object = Coupon.objects.get(coupon_code=code, is_available=True)
            coupon_user = CouponUsers()
            coupon_user.user    = request.user
            coupon_user.coupon  = coupon_object
            coupon_user.is_used = False
            coupon_user.amount  = coupon_object.amount
            coupon_user.save()
            print("0000000000000000000")
            print(coupon_user.amount)

            coupon_object.quantity -= 1
            if coupon_object.quantity == 0:
                coupon_object.is_available = False
            coupon_object.save() 
        else:
            
            return redirect(cart)  
            
    return redirect(cart)