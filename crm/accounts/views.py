from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from .models import *
from .forms import *
from .filters import OrderFilter
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decoraters import *
from django.contrib.auth.models import Group

@unauth_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        #authenticates the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) #django inbuilt login fucntion
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)
    

@unauth_user
def register(request):
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            #grabs the new user and makes it a member of customer group
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            #this makesthe user a customer object with all inital vals for internal parameters
            Customer.objects.create(
                user=user,
                name=user.username,
            )

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context={'form':form}
    return render(request,'accounts/register.html',context)


def logoutUser(request):
	logout(request) #django inbuilt logout function
	return redirect('login')

@login_required(login_url='login')
@allowed_user(['admin'])
def home(request):
    customer=Customer.objects.all()
    orders=Order.objects.all()
    #username=customer.get('username')
    order_cnt=orders.count()
    customer_cnt=customer.count()
    orders_pending=orders.filter(status='Pending').count()
    order_delivered=orders.filter(status='Delivered').count()

    context={'Customer_dict':customer,'Order_dict':orders,'pending':orders_pending,'delivered':order_delivered,
             'order_count':order_cnt}
    #'Customer_dict' is going to be refrenced in html files
    #on refrencing iyt in htmlfiles you can excel :customer value in the context
    return render(request,'accounts/dashboard.html',context)
    #context is used to pass in multiple parameters

@login_required(login_url='login')
@allowed_user(['admin'])
def product(request):
    #from product model gets all products from the db
    Products=Product.objects.all()
    return render(request,'accounts/products.html',{'Product_dict':Products})
    #here {'Product_dict':Products} is bascialyy the context bus as its only 1 parameter we didnt 
    #store it in the context and vaiable and pass it like in home() function

@login_required(login_url='login')
@allowed_user(['admin'])
#building a filter in this tofilter out th products of the customer
def customer(request,key):
    #key is the string value id which we need to dynamically load on the customer route
    #check urls.py customer route <str:key> will load the specific customers page inside customer.html
    customer=Customer.objects.get(id=key)
    order=customer.order_set.all()
    order_cnt=order.count()
    #order_cnt=customer.order

    myFilter=OrderFilter(request.GET, queryset=order)
    order=myFilter.qs


    context={'customer':customer,'Orders':order,'order_cnt':order_cnt, 'myFilter':myFilter}
    return render(request,'accounts/customer.html',context) 

@login_required(login_url='login')
def CreateOrder(request,key):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=4)
    customer=Customer.objects.get(id=key)
    #form=OrderForm(initial={'customer':customer})
    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method=='POST':
        form=OrderForm(request.POST)
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')     
           
    context={'form':formset}
    return render(request,'accounts/order_form.html',context)


@login_required(login_url='login')
def DeleteOrder(request,key):
    order=Order.objects.get(id=key)
    order_name=order.product.name
    if request.method=='POST':
       order.delete()
       return redirect('/')

    context={'order':order,'item':order_name}
    return render(request,'accounts/delete.html',context)

@login_required(login_url='login')
def UpdateOrder(request,key):
    order=Order.objects.get(id=key)
    form=OrderForm(instance=order)
    if request.method=='POST':
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}

    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
def CreateCustomer(request):
    form=CustomerForm()
    if request.method=='POST':
         form=CustomerForm(request.POST)
         if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
def UpdateCustomer(request,key):
    customer=Customer.objects.get(id=key)
    form=CustomerForm(instance=customer)
    if request.method=='POST':
        form=CustomerForm(request.POST,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'accounts/order_form.html',context)
	 
@login_required(login_url='login')
def deleteCustomer(request,key):
    customer=Customer.objects.get(id=key)
    customer_name=customer.name
    context={'item':customer_name}
    if request.method=='POST':
        customer.delete()
        return redirect('/')
    
    return render(request, 'accounts/delete.html',context)
    

@login_required(login_url='login')
@allowed_user(['customer'])
def userProfile(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    print('ORDERS:', orders,total_orders)

    context = {'orders':orders, 'order_count':total_orders,'delivered':delivered,'pending':pending}
    return render(request, 'accounts/user.html', context)
