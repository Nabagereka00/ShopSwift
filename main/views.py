from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem
from django.contrib import messages

def home(request):
    products = Product.objects.all()
    return render(request, 'main/home.html',{'products': products})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1
    request.session['cart'] = cart
    return redirect('cart')

def cart_view(request):
    cart = request.session.get('cart',{})
    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=int(product_id))
        item_total = product.price * quantity
        products.append({
            'product': product,
            'quantity': quantity,
            'total': item_total})
        total += item_total

    return render(request, 'main/cart.html', {'products': products, 'total': total})

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id = str(item_id)
    if item_id in cart:
        del cart[item_id]
        request.session['cart'] = cart
        request.session.modified = True
        return redirect('cart')

def update_cart(request, product_id, action):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        if action =='increase':
            cart[product_id] += 1
        elif action =='decrease':
            cart[product_id] -= 1
            if cart[product_id] <= 0:
                del cart[product_id]
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

def checkout_view(request):
    cart = request.session.get('cart', {})
    
    if not cart:
        return redirect('home')
    
    products = []
    total = 0
    cart_items_text = ""

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=int(product_id))
        item_total = product.price * quantity
        products.append({
            'product': product,
            'quantity': quantity,
            'total': item_total
        })
        total += item_total
        cart_items_text += f"{product.name} x{quantity} = UGX {item_total}\n"

    if request.method =='POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        otp = request.POST.get('otp')

        if otp != '123456':
            messages.error(request, 'Wrong OTP. Please use 123456')
            return redirect('/checkout/')
        
        cart_items_text =""




        order = Order.objects.create(
            name=name,
            phone=phone,
            address=address,
            total=total,
        )
            

        for product_id, qty in cart.items():
            product = Product.objects.get(id=int(product_id))
            OrderItem.objects.create(
            order =order,
            product=product,
            quantity=qty,
            price=product.price
        )

        
        request.session['cart'] = {}
        request.session.modified = True


        return render(request, 'main/order_success.html' , {'name': name, 'total': total})
    
    context ={
        'products': products,
        'total': total
    }

    return render(request, 'main/checkout.html', context)



def about(request):
    return render(request, 'about.html')

def products(request):
    products = Product.objects.all()
    return render(request, 'main/products.html', {'products': products})

def cart(request):
    return render(request, 'cart.html')

def contact(request):
    return render(request, 'contact.html')

# Create your views here.
