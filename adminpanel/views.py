
from django.shortcuts import render,redirect
from accounts . models import Account
from category . models import category
from adminpanel . forms import CategoryForm
from django.contrib import messages
from django.template.defaultfilters import slugify
from orders . models import Order,OrderProduct,Payment
from orders . models import Product,Variation
from adminpanel . forms import ProductForm
from adminpanel . forms import VariationForm

from django.contrib.auth.decorators import login_required 
# Create your views here.

def adminpanel(request):
    if request.user.is_superadmin:
        return render(request,'adminpanel/adminpanel.html')
    else:
        return redirect('home')

def admin_login(request):
    return render(request,'adminpanel/admin_accounts/admin_login.html')
    

@login_required(login_url ='login')
def user_accounts_table(request):
    if request.user.is_superadmin:
        active_users = Account.objects.all().filter(is_admin=False,is_active=True)
        banned_users = Account.objects.all().filter(is_admin = False, is_active =False)
        context  = {
            'active_users' : active_users,
            'banned_users' : banned_users,
        }
        return render(request,'adminpanel/admin_accounts/accounts.html',context)
    else:
        return redirect('home')

@login_required(login_url ='login')
def ban_user(request,id):
    if request.user.is_superadmin:
        user           = Account.objects.get(id=id)
        user.is_active = False
        user.save()
        return redirect('user_accounts_table')
    else:
        return redirect('home')

@login_required(login_url ='login')
def unban_user(request,id):
    if request.user.is_superadmin:
        user           = Account.objects.get(id=id)
        user.is_active = True
        user.save()
        return redirect('user_accounts_table')
    else:
        return redirect('home')

@login_required(login_url ='login')
def category_table(request):
    if request.user.is_superadmin:
        categorys=category.objects.all()
        context={
            'categorys':categorys,
        }
        return render(request,'adminpanel/category_table/category_table.html',context)
    else:
        return redirect('home')

@login_required(login_url ='login')
def addcategory(request):
    if request.user.is_superadmin:
        form = CategoryForm()
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                categorys = form.save()
                category_name = form.cleaned_data['category_name']
                slug = slugify(category_name)
                categorys.slug = slug
                categorys.save()
                messages.success(request,'New category added successfully')
                return redirect('category_table')
        context = {
            'form' : form,
        }
        return render (request,'adminpanel/category_table/add_category.html',context)
    else:
        return redirect('home')


@login_required(login_url ='login')
def editcategory(request,id):
    if request.user.is_superadmin:
        categorys = category.objects.get(id=id)
        if request.method == 'POST':
            form = CategoryForm(request.POST,request.FILES,instance=categorys)
            if form.is_valid():
                category_name = form.cleaned_data['category_name']
                slug = slugify(category_name)
                categoryss = form.save()
                categoryss.slug = slug
                categoryss.save()
                messages.success(request,'category editted successfully')
                return redirect('category_table')
        else:
            form = CategoryForm(instance=categorys)
        context = {
            'form' : form,
        }
        return render(request,'adminpanel/category_table/add_category.html',context)
    else:
        return redirect('home')


@login_required(login_url ='login')
def deletecategory(request,id):
    if request.user.is_superadmin:
        categorys=category.objects.get(id=id)
        categorys.delete()
        return redirect('category_table')
    else:
        return redirect('home')

@login_required(login_url ='login')
def order_table(request,id):
    if request.user.is_superadmin:
        orders = Order.objects.filter(is_ordered=True,status='New')
        accepted_orders = Order.objects.filter(is_ordered=True,status='Accepted')
        completed_orders = Order.objects.filter(is_ordered=True,status="Completed")
        cancelled_orders = Order.objects.filter(is_ordered=True,status="Cancelled")
        order_products = OrderProduct.objects.all()
        payments = Payment.objects.all()
        context = {
            'orders' : orders,
            'order_products' : order_products,
            'payments' : payments,
            'accepted_orders' : accepted_orders,
            'completed_orders' : completed_orders,
            'cancelled_orders' : cancelled_orders,
        }

        if id==1:
            return render (request,'adminpanel/order_table/orders.html',context)
        elif id==2:
            return render(request,'adminpanel/order_table/order_products.html',context)   
        elif id==3:
            return render(request,'adminpanel/order_table/accepted_orders.html',context)
        elif id==4:
            return render(request,'adminpanel/order_table/completed_orders.html',context)
        elif id==5:
            return render(request,'adminpanel/order_table/cancelled_orders.html',context)
        else:
            return render(request,'adminpanel/order_table/payments.html',context)
    else:
        return redirect('home')

@login_required(login_url ='login')
def order_accepted(request,order_id):
    if request.user.is_superadmin:
        order = Order.objects.get(id=order_id)
        order.status = 'Accepted'
        order.save()
        return redirect('order_table',id=3)
    else:
        return redirect ('home')

@login_required(login_url ='login')
def order_completed(request,order_id):
    if request.user.is_superadmin:
        order=Order.objects.get(id=order_id)
        order.status = 'Completed'
        order.save()
        return redirect('order_table',id=2)
    else:
        return redirect('home')


@login_required(login_url ='login')
def order_cancelled(request,order_id):
    if request.user.is_superadmin:
        order=Order.objects.get(id=order_id)
        order.status = 'Cancelled'
        order.save()
        return redirect('order_table',id=1 )
    else:
        return render(request,'adminpanel/order_table/order_cancelled.html')

@login_required(login_url ='login')
def store_table(request,id):
    if request.user.is_superadmin:
        products = Product.objects.all()
        variations =Variation.objects.all()

        context = {
            'products' : products,
            'variations' : variations,
        }
        if id==1:
            return render(request,'adminpanel/store_table/products.html',context)
        else:
            return render(request,'adminpanel/store_table/variations.html',context)
    else:
        return redirect('home')

@login_required(login_url ='login')
def add_product(request):
    if request.user.is_superadmin:
        form = ProductForm()
        if request.method == 'POST':
            form = ProductForm(request.POST,request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product_name = form.cleaned_data['product_name']
                slug = slugify(product_name)
                product.slug = slug
                product.save()

                
                return redirect('store_table',id=1)
        else:
            form = ProductForm()
        context = {
            'form' : form,
        }
        return render(request,'adminpanel/store_table/add_product.html',context)
    else:
        return redirect('home')

@login_required(login_url ='login')
def edit_product(request,id):
    if request.user.is_superadmin:
        product = Product.objects.get(id=id)
        if request.method =='POST':
            form = ProductForm(request.POST,request.FILES,instance=product)
            if form.is_valid():
                product_name = form.cleaned_data['product_name']
                slug = slugify(product_name)
                product = form.save()
                product.slug = slug
                product.save()

                
                return redirect('store_table',id=1)
        else:
            form = ProductForm(instance=product)
        context = {
            'form' : form,

        }
        return render (request,'adminpanel/store_table/add_product.html',context)
    else:
        return redirect ('home')


@login_required(login_url ='login')
def delete_product(request,id):
    if request.user.is_superadmin:
        product = Product.objects.get(id=id)
        product.delete()
        return redirect('store_table',id=1)
    else:
        return redirect ('home')

@login_required(login_url ='login')
def add_variations(request):
    if request.user.is_superadmin:
        form = VariationForm()
        if request.method == 'POST':
            form = VariationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('store_table',id=2)
        else:
            form = VariationForm()
        context = {
            'form' : form,
        }
        return render(request,'adminpanel/store_table/add_variations.html',context)
    else:
        return redirect('home')





@login_required(login_url ='login')
def delete_variations(request,id):
    if request.user.is_superadmin:
        variation = Variation.objects.get(id=id)
        variation.delete()
        return redirect('store_table',id=2)
    else:
        return redirect ('home')
