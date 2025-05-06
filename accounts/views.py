from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User, auth
from django.db import connection  
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from .models import Products,Cart,CustomerInfo,OrderHistory,ProductReview
import json
from django.utils.timezone import now, timedelta
from datetime import datetime
from decimal import Decimal

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password, 
                                        email=email, first_name=first_name, last_name=last_name)
                user.save()
                
                return redirect('login_user')


        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect('register')
            

    else:
        return render(request, 'registration.html')
    

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.get_messages(request)  
            return redirect('home')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login_user')
    else:
        return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def logout_user(request):
    auth.logout(request)
    return redirect('home')

def product_list(request,category):
    colors = request.GET.getlist('color')  
    materials = request.GET.getlist('material')  
    brands = request.GET.getlist('brand')  
    sort_option = request.GET.get('sort', '')  
    page = request.GET.get('page', 1) 
    try:
        page = int(page)  
    except ValueError:
        page = 1 
    # Base query
    query = "SELECT * FROM accounts_products WHERE category = %s"
    params = [category]

    # Filtering by color
    if colors:
        placeholders = ", ".join(["%s"] * len(colors))
        query += f" AND color IN ({placeholders})"
        params.extend(colors)

    # Filtering by material
    if materials:
        placeholders = ", ".join(["%s"] * len(materials))  
        query += """ 
            AND (
                CASE 
                    WHEN material LIKE 'cotton%%' THEN 'cotton'
                    WHEN material LIKE 'wool%%' THEN 'wool'
                    WHEN material LIKE 'silk%%' THEN 'silk'
                    WHEN material LIKE '%%gold%%' then 'gold'
                    WHEN material LIKE '%%silver%%' then 'silver'
                    WHEN material LIKE '%%metal%%' then 'metal'
                    ELSE material
                END IN ({})
            )
        """.format(placeholders)
        params.extend(materials)

    # Filtering by brand
    if brands:
        placeholders = ", ".join(["%s"] * len(brands))
        query += f" AND brand IN ({placeholders})"
        params.extend(brands)

    # Sorting
    if sort_option == "price_high":
        query += " ORDER BY mrp DESC"
    elif sort_option == "price_low":
        query += " ORDER BY mrp ASC"
    elif sort_option == "name_az":
        query += " ORDER BY product_name ASC"
    elif sort_option == "name_za":
        query += " ORDER BY product_name DESC"

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        # products = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        products = [dict(zip(columns, row)) for row in cursor.fetchall()]

    paginator = Paginator(products, 10)
    page_obj = paginator.get_page(page)

    query_params = request.GET.copy()
    if "page" in query_params:
        del query_params["page"]  # Remove old page numbers

    # Get distinct filter values from database
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT color FROM accounts_products WHERE color IS NOT NULL AND category = %s", [category])
        all_colors = [row[0] for row in cursor.fetchall() if row[0]]

        cursor.execute("SELECT DISTINCT material FROM accounts_products WHERE material IS NOT NULL AND category = %s", [category])
        all_materials = [row[0] for row in cursor.fetchall() if row[0]]

        cursor.execute("SELECT DISTINCT brand FROM accounts_products WHERE brand IS NOT NULL AND category = %s", [category])
        all_brands = [row[0] for row in cursor.fetchall() if row[0]]

    return render(request, 'product_list.html', {
        'page_obj': page_obj,
        'selected_colors': colors,
        'selected_materials': materials,
        'selected_brands': brands,
        'selected_sort': sort_option,
        'category': category,
        'request_params': query_params.urlencode(),  
        'colors': all_colors,         # ✅ from DB
        'materials': all_materials,   # ✅ from DB
        'brands': all_brands       
    })

def contents(request):
    return render(request, 'contents.html')

def myproduct(request, product_id):
    product = get_object_or_404(Products, product_id=product_id)
    return render(request, 'myproduct.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, product_id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 0))
        cart_item.quantity += quantity
        cart_item.save()

    return redirect("view_cart")

@login_required
def view_cart(request):

    cart_items = Cart.objects.filter(user=request.user).select_related("product")

    if not cart_items.exists():
        messages.info(request, "Your cart is empty.")

    cart_total = sum(item.product.mrp * item.quantity for item in cart_items)
    sales_tax = 0.05 * float(cart_total)  
    shipping_fee = 5 if cart_total < 100 else 0
    grand_total = float(cart_total) + sales_tax + shipping_fee

    print("Cart Items:", cart_items)  
    for item in cart_items:
        print(f"Product: {item.product.product_name}, Quantity: {item.quantity}")

    context = {
        "cart_items": cart_items,
        "cart_total": round(cart_total, 2),
        "sales_tax": round(sales_tax, 2),
        "shipping_fee": shipping_fee,
        "grand_total": round(grand_total, 2),
    }
    
    return render(request, "cart.html", context)


@csrf_exempt
@login_required
def remove_from_cart(request, product_id):
    item = get_object_or_404(Cart, id=product_id, user=request.user)
    item.delete()
    return JsonResponse({"success": True, "message": "Item removed successfully"})


@csrf_exempt
@login_required
def update_cart(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(Cart, id=item_id, user=request.user)
        action = request.POST.get("action")
        
        if action == "increase":
            if item.quantity >= item.product.stock:
                return JsonResponse({
                    "success": False,
                    "message": "Stock limit reached",
                    "stock": item.product.stock
                })
            item.quantity += 1
        elif action == "decrease":
            if item.quantity > 1:
                item.quantity -= 1
            else:
                item.delete()
                return cart_data(request)
        
        item.save()
        cart_items = Cart.objects.filter(user=request.user).select_related('product')
        cart_list = [
            {
                "id": item.id,
                "product_name": item.product.product_name,
                "price": float(item.product.mrp),
                "quantity": item.quantity,
                "stock": item.product.stock,  # Include stock info
                "image": item.product.image,
            }
            for item in cart_items
        ]
        cart_total = sum(item["price"] * item["quantity"] for item in cart_list)
        sales_tax = 0.05 * cart_total
        shipping_fee = 5 if cart_total < 100 else 0
        grand_total = cart_total + sales_tax + shipping_fee

        return JsonResponse({
            "success": True,
            "cart_items": cart_list,
            "cart_total": round(cart_total, 2),
            "sales_tax": round(sales_tax, 2),
            "shipping_fee": shipping_fee,
            "grand_total": round(grand_total, 2),
        })
    
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect("view_cart")  # Redirect if cart is empty

    order_total = sum(item.product.mrp * item.quantity for item in cart_items)

    return render(request, "payment.html", {"order_total": order_total})

@login_required
def cart_data(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_list = [
        {
            "id": item.id,
            "product_name": item.product.product_name,
            "price": float(item.product.mrp),
            "quantity": item.quantity,
            "image": item.product.image,
        }
        for item in cart_items
    ]
    cart_total = sum(item["price"] * item["quantity"] for item in cart_list)
    sales_tax = 0.05 * cart_total
    shipping_fee = 5 if cart_total < 100 else 0
    grand_total = cart_total + sales_tax + shipping_fee

    return JsonResponse({
        "cart_items": cart_list,
        "cart_total": round(cart_total, 2),
        "sales_tax": round(sales_tax, 2),
        "shipping_fee": shipping_fee,
        "grand_total": round(grand_total, 2),
    })

@login_required
def payment_view(request):
    user = request.user
    customer_info = CustomerInfo.objects.filter(customerid=user).first()

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name', '')
        apartment_number = request.POST.get('apartment_number')
        street_name = request.POST.get('street_name')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pincode = request.POST.get('pincode')
        payment_mode = request.POST.get('payment_mode')

        if customer_info:
            # Update existing record
            customer_info.first_name = first_name
            customer_info.last_name = last_name
            customer_info.apartment_number = apartment_number
            customer_info.street_name = street_name
            customer_info.city = city
            customer_info.state = state
            customer_info.country = country
            customer_info.pincode = pincode
            customer_info.payment_mode = payment_mode
            customer_info.save()
        else:
            # Create new record
            CustomerInfo.objects.create(
                customerid=user,
                first_name=first_name,
                last_name=last_name,
                apartment_number=apartment_number,
                street_name=street_name,
                city=city,
                state=state,
                country=country,
                pincode=pincode,
                payment_mode=payment_mode
            )

        return redirect('/accounts/confirmation/')  # Redirect to a confirmation page

    return render(request, "payment.html", {"customer": customer_info})

def payment(request):
    return render(request, 'payment.html')



@login_required
def order_history(request):
    orders = OrderHistory.objects.filter(user=request.user).select_related('product')

    order_data = []
    for order in orders:
        order_data.append({
            'id': order.id,
            'quantity': order.quantity,
            'order_date': order.order_date,
            'product_name': order.product.product_name,
            'product_image': order.product.image
        })

    return render(request, 'order_history.html', {'orders': order_data})

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    
    if request.method == "POST":
        name = request.POST.get("name")
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")
        
        if name and rating and comment:
            ProductReview.objects.create(
                product=product,
                name=name,
                rating=int(rating),
                comment=comment
            )
            messages.success(request, "Thank you for your review!")
        else:
            messages.error(request, "All fields are required.")
        
        return redirect("product_detail", product_id=product.id)
    
    return redirect("product_detail", product_id=product.id)

@login_required
@csrf_exempt
def submit_review(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            reviews = data.get('reviews', [])

            # Convert reviews list to dict for easy lookup
            review_dict = {str(r['product_id']): r for r in reviews}

            for cart_item in cart_items:
                product = cart_item.product
                quantity_purchased = cart_item.quantity

                # Check if there's a review for this product
                review_data = review_dict.get(str(product.product_id))
                if review_data:
                    rating = review_data.get("rating")
                    review_text = review_data.get("review_text", "")
                    ProductReview.objects.create(
                        customer=user,
                        product=product,
                        rating=int(rating),
                        review_text=review_text
                    )

                # Always update stock
                product.stock = max(product.stock - quantity_purchased, 0)
                if product.stock == 0:
                    product.availability = 0
                product.save()

            # Clear the cart
            cart_items.delete()

            return JsonResponse({"message": "Stock updated. Reviews saved where provided."})

        except Exception as e:
            return JsonResponse({"message": f"Error: {str(e)}"}, status=400)

    return JsonResponse({"message": "Invalid request"}, status=400)

@login_required
def order_confirmation(request):
    user = request.user

    customer_name = request.user.get_full_name() or request.user.username  
    order_date = datetime.now()
    shipping_date = order_date + timedelta(days=3)
    cart_items = Cart.objects.filter(user=request.user)


    cart_total = sum(item.product.mrp * item.quantity for item in cart_items)
    sales_tax = Decimal('0.05') * cart_total   
    shipping_fee = 5 if cart_total < 100 else 0 
    grand_total = round(float(cart_total) + float(shipping_fee)+float(sales_tax),2)

    for item in cart_items:
        item.total_price = item.product.mrp * item.quantity
    context = {
        "customer_name": customer_name,
        "order_date": order_date.strftime("%Y-%m-%d %H:%M:%S"),
        "shipping_date": shipping_date.strftime("%Y-%m-%d"),
        "cart_items": cart_items,
        "cart_total": cart_total,
        "shipping_fee": shipping_fee,
        "grand_total": grand_total,
    }
    print("Order Date:", order_date)
    if cart_items.exists():
        for item in cart_items:
            OrderHistory.objects.create(
                user=user,
                product=item.product,
                quantity=item.quantity
            )

    return render(request, "confirmation.html", context)
