from django.shortcuts import render, redirect
from django.views import View
from . models import Product,Customer,Cart, OrderPlaced
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect
from django.db.models import Q
from .models import Cart, Product , banner


    

class ProductView(View):
    def get(self, request):
        all_product = Product.objects.all()
        banners = banner.objects.all()
        if request.user.is_authenticated:
         carts_count = Cart.objects.filter(user=request.user).count()
         return render(request, 'Shop/home.html', {'banners':banners,'a':carts_count,'all_product':all_product})
         
        
        return render(request, 'Shop/home.html', {'banners':banners,'all_product':all_product})



def minuscart(request):
    if request.method == 'GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      
      c.quantity -=1
      c.save()
      amount = 0.0
      shipping_amount = 100.0
      cart_product = [p for p in Cart.objects.all() if p.user==request.user]
      for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount  
            totalamount = amount + shipping_amount
      data = {
         'quantity': c.quantity,
         'amount': amount,
         'totalamount': totalamount
      }
      return JsonResponse(data)
    
def plus_cart(request):
    if request.method == 'GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      
      c.quantity +=1
      c.save()
      amount = 0.0
      shipping_amount = 100.0
      cart_product = [p for p in Cart.objects.all() if p.user==request.user]
      for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount  
            totalamount = amount + shipping_amount
      data = {
         'quantity': c.quantity,
         'amount': amount,
         'totalamount': totalamount
      }
      return JsonResponse(data)
    
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from .models import Cart

def removecart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        
        # Get the cart item for the specific product and user, if it exists
        try:
            cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Product not found in cart'}, status=404)
        # Check if this is the only item in the cart
        cart_product_count = Cart.objects.filter(user=request.user).count()
        # If only one item is in the cart, delete it and render the empty cart page
        if cart_product_count == 1:
                    cart_item.delete()
                    data = {
            'amount': 0,
            'totalamount': 100}
                    return JsonResponse(data)
        
        # If more than one item, delete the selected item and calculate the updated amounts
        cart_item.delete()
        
        amount = 0.0
        shipping_amount = 100.0
        cart_products = Cart.objects.filter(user=request.user)
        
        for item in cart_products:
            tempamount = item.quantity * item.product.discounted_price
            amount += tempamount
        totalamount = amount + shipping_amount

        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        
        return JsonResponse(data)

            
           
            
            
      



class ProductDetailView(View):
  def get(self,request, pk):
    product = Product.objects.get(pk=pk)
    if request.user.is_authenticated:
         carts_count = Cart.objects.filter(user=request.user).count()
         return render(request, 'Shop/productdetail.html', {'a':carts_count,'product': product})
    return render(request, 'Shop/productdetail.html',{'product': product})




@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    # Check if the product is already in the cart for this user
    Cart.objects.get_or_create(user=user, product=product)
    return redirect('/cart')

@login_required
def show_cart(request):
   if request.user.is_authenticated:
           
      carts_count = Cart.objects.filter(user=request.user).count()
      
      user = request.user
      cart = Cart.objects.filter(user=user)
      amount = 0.0
      shipping_amount = 100.0
      total = 0.0
      cart_product = [p for p in Cart.objects.all() if p.user==user]
      if cart_product:
         for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount  
            totalamount = amount + shipping_amount
         return render(request, 'Shop/addtocart.html', {'carts':cart,'a':carts_count, 'totalamount':totalamount,'amount':amount })
      else:
         return render(request, 'Shop/emptycart.html')

def buy_now(request):
 return render(request, 'Shop/buynow.html')

@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    def get(self, request):
      form = CustomerProfileForm
      a = Cart.objects.filter(user=request.user).count()
      return render(request, 'Shop/profile.html', {'form':form,'a':a, 'active':'btn-primary'})
   
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            division = form.cleaned_data['division']
            district = form.cleaned_data['district']
            thana = form.cleaned_data['thana']
            villorroad = form.cleaned_data['villorroad']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name, division=division,district=district, thana=thana, villorroad=villorroad, zipcode=zipcode)
            reg.save()
            
      
            messages.success(request, 'Congratulations! Profile Updated Successfully')
        return render(request, 'Shop/profile.html', {'form':form ,'active':'btn-primary'})

@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 a = Cart.objects.filter(user=request.user).count()
 print(add)
 if  add.exists():
    return render(request, 'Shop/address.html', {'add':add, 'active':'btn-primary' , 'd':"none"})
 return render(request, 'Shop/address.html', {'a':a,'d':'Block'})

@login_required
def payment(request):
    Customer_id = request.GET.get('address')
    customer = Customer.objects.get(id=Customer_id)
    cart = Cart.objects.filter(user=request.user)
    for cart in cart:
        OrderPlaced(user=request.user, customer=customer, product=cart.product, quantity=cart.quantity).save()
        cart.delete()
    return redirect('/orders')

def orders(request):
    all_products_user = OrderPlaced.objects.filter(user=request.user)
    a = Cart.objects.filter(user=request.user).count()
   
    
    return render(request, 'Shop/orders.html' , {'a':a,"ab":all_products_user})



def lehenga(request, data =None):
    if data == None:
        lehengas = Product.objects.filter(category = 'L')
    elif data == 'lubnan' or data == 'infinity':
        lehengas = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        lehengas = Product.objects.filter(category='L').filter(discounted_price__lt=20000)
    elif data == 'above':
        lehengas = Product.objects.filter(category='L').filter(discounted_price__gt=20000)
    return render(request, 'Shop/lehenga.html', {'lehengas':lehengas})



class CustomerRegistrationView(View):
  def get(self,request):
     form = CustomerRegistrationForm()
     return render(request, 'Shop/customerregistration.html', {'form':form})
  
  def post(self,request):
     form = CustomerRegistrationForm(request.POST)
     
     if form.is_valid():
        messages.success(request,'Congratulations registration done.')
        form.save()
     return render(request, 'Shop/customerregistration.html', {'form':form})
 
@login_required
def checkout(request):
 if request.user.is_authenticated:
    Customers = Customer.objects.filter(user=request.user)
    Carts = Cart.objects.filter(user=request.user)
    a = Cart.objects.filter(user=request.user).count()
    
    total_product = [product for product in Cart.objects.filter(user=request.user) ]
    total = 0
    for i in total_product:
        total += i.total_price
    
        

    return render(request, 'Shop/checkout.html', {'c':Customers ,'a':a, "carts":Carts , 'total':total})

from django.http import JsonResponse

def remove_address(request):
    address_id = request.GET.get('prod_id')
    print(address_id)
    Customer.objects.filter(id=address_id, user=request.user).delete()
    
    remaining_count = Customer.objects.filter(user=request.user).count()
    if remaining_count == 0:
        return JsonResponse({'status': "no_address"})
    else:
        return JsonResponse({'status': "success"})
