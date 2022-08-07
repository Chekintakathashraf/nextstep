

from django.shortcuts import render,redirect
from carts.models import CartItem
from orders.forms import OrderForm
from orders.models import Order, OrderProduct, Payment
from store.models import Product
import razorpay
from nextstep.settings import RAZOR_KEY_ID,KEY_SECRET

import datetime
import json
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.template.loader import render_to_string

from coupon.models import CouponUsers,Coupon
# Create your views here.



def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['order_number'])
    
    payment = Payment(
        user = request.user,
        payment_id = body['razorpay_payment_id'],
        amount_paid = body['amount_paid'],
        status = body['status'],
        payment_method = body['payment_method']
    )
    payment.save()
    order.payment = payment 
    order.is_ordered = True
    order.save()
    
    # move the cart items to order product table

    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        #product save
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        #variation save
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        #reduce the quantity of sold product
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    #clear cart
    CartItem.objects.filter(user=request.user).delete()

    #send order recieved email
    mail_subject = 'Thank You. Your order has been recieved'
    message = render_to_string('orders/order_recieved_email.html',{
        'user':request.user,
        'order':order,
        # 'domain':current_site,
        # 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        # 'token':default_token_generator.make_token(user)
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()


    data = {
        'order_number': order.order_number,
        'payment_id': payment.payment_id,
    }
    return JsonResponse(data)


def place_order(request, total=0, quantity=0):

    current_user = request.user

# if the cart count is less than or equal to 0, then redirect back to store

    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    # tax = (2 * total)/100
    # grand_total = total + tax

    if CouponUsers.objects.filter(user=request.user, is_used= False).exists() :
        coupon_user = CouponUsers.objects.get(user=request.user, is_used= False)
        print('----------------------------')
        print(coupon_user)
        coupon      = coupon_user.amount if total >= 500 else 0
    tax = (2 * total/100 )
    grand_total = total + tax - coupon



    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # store all the billing informataion indide order table
            data = Order()
           
            data.user = current_user
            data.first_name      = form.cleaned_data['first_name']
            data.last_name       = form.cleaned_data['last_name']
            data.phone           = form.cleaned_data['phone']
            data.email           = form.cleaned_data['email']
            data.address_line_1  = form.cleaned_data['address_line_1']
            data.address_line_2  = form.cleaned_data['address_line_2']
            data.country         = form.cleaned_data['country']
            data.state           = form.cleaned_data['state']
            data.city            = form.cleaned_data['city']
            data.order_total     = grand_total
            data.tax             = tax
            data.ip              = request.META.get('REMOTE_ADDR')


            data.save()


            # Generate order number

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d  = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") # eg 20201027  yearmmonthdate
            
            order_number = current_date + str(data.id)
           
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)


#razor pay work


            client = razorpay.Client(auth=(RAZOR_KEY_ID,KEY_SECRET))

            data = { 
                "amount": int(order.order_total*100),
             "currency": "INR",
              "receipt": "order_rcptid_11" 
              }

            payment = client.order.create(data=data)
 

 # until 

            context = {
                'payment':payment,
                'order':order,
                'cart_items' : cart_items,
                'total' : total,
                'tax' : tax,
                'grand_total' : grand_total,
                'coupon' : coupon,
            }

            return render(request, 'orders/payments.html',context)
    
    else:
        return redirect('checkout')


def order_complete(request):
    # return render(request,'orders/order_complete.html')
    order_id=request.GET.get('order_id')
    transID=request.GET.get('payment_id')
    try:
        order=Order.objects.get(order_number=order_id,is_ordered=True)
        ordered_product=OrderProduct.objects.filter(order_id=order.id)

        subtotal=0
        for i in ordered_product:
            subtotal+=i.product_price * i.quantity

        payment=Payment.objects.get(payment_id=transID)
        context={
            'order':order,
            'order_number':order.order_number,
            'ordered_product':ordered_product,
            'transID':payment.payment_id,
            'payment':payment,
            'sub_total':subtotal,
        }
        return render(request,'orders/order_complete.html',context)
    except(Order.DoesNotExist,Payment.DoesNotExist):
        return redirect('home')