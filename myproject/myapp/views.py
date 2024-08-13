from tkinter import Canvas
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def order(request):
    return render(request, 'order.html')

def popular_menu(request):
    return render(request, 'popular_menu.html')

def reorder(request):
    return render(request, 'reorder.html')

def review(request):
    return render(request, 'review.html')

def reservation(request):
    return render(request, 'reservation.html')

def admin_page(request):
    return render(request, 'admin.html')

def manager(request):
    return render(request, 'manager.html')

def staff(request):
    return render(request, 'staff.html')

def know_the_food_taste(request):
    return render(request, 'know_the_food_taste.html')

def location(request):
    return render(request, 'location.html')



import json

# myapp/views.py
from django.shortcuts import render, get_object_or_404
from .models import MenuItem, Category

def menu(request, category=None):
    categories = Category.objects.all()

    if category is None:
        if categories.exists():
            current_category = categories.first()
        else:
            current_category = None
    else:
        current_category = get_object_or_404(Category, name=category)

    items = MenuItem.objects.filter(category=current_category) if current_category else []

    context = {
        'categories': categories,
        'items': items,
        'current_category': current_category.name if current_category else 'No Categories Available'
    }
    return render(request, 'menu.html', context)



from django.shortcuts import render
import json

def order(request):
    if request.method == 'POST':
        selected_items = json.loads(request.POST.get('selected_items', '[]'))
    else:
        selected_items = []

    order_items = []
    subtotal = 0

    for item in selected_items:
        name = item['name']
        price = float(item['price'])
        quantity = int(item.get('quantity', 1))
        total = price * quantity
        order_items.append({'name': name, 'price': price, 'quantity': quantity, 'total': total})
        subtotal += total

    sales_tax = subtotal * 0.1025
    grand_total = subtotal + sales_tax

    context = {
        'order_items': order_items,
        'subtotal': subtotal,
        'sales_tax': sales_tax,
        'grand_total': grand_total
    }
    return render(request, 'order.html', context)



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm
from .models import MyUser

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid phone number or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')



from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import MyUser, Order
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password

def admin_login(request):
    if request.method == "POST":
        password = request.POST.get('password')
        if password == "tanviR1243":
            return redirect('custom_admin')
        else:
            return HttpResponse("Invalid password", status=401)
    return render(request, 'admin_login.html')

def admin_page(request):
    return render(request, 'admin.html')

def manage_users(request):
    users = MyUser.objects.all()
    return render(request, 'manage_users.html', {'users': users})

@csrf_exempt
def add_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        password = make_password(request.POST.get('password'))
        MyUser.objects.create(username=username, name=name, phone=phone, password=password)
        return redirect('manage_users')

@csrf_exempt
def edit_user(request, user_id):
    user = get_object_or_404(MyUser, id=user_id)
    if request.method == "POST":
        user.username = request.POST.get('username')
        user.name = request.POST.get('name')
        user.phone = request.POST.get('phone')
        new_password = request.POST.get('new_password')
        if new_password:
            user.password = make_password(new_password)
        user.save()
        return redirect('manage_users')

@csrf_exempt
def delete_user(request, user_id):
    user = get_object_or_404(MyUser, id=user_id)
    if request.method == "POST":
        user.delete()
        return redirect('manage_users')

def manage_staff(request):
    return render(request, 'manage_staff.html')

def manage_reservations(request):
    return render(request, 'manage_reservations.html')

def manage_orders(request):
    orders = Order.objects.all()
    return render(request, 'manage_orders.html', {'orders': orders})

# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ReservationForm
from .models import Reservation

@login_required
def reserve_table(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            request.session['reservation_id'] = reservation.id
            return redirect('reservation_success')  # Update to the appropriate success URL
    else:
        form = ReservationForm()
    return render(request, 'reservation.html', {'form': form})

def manage_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'manage_reservations.html', {'reservations': reservations})

@login_required
def reservation_success(request):
    reservation_id = request.session.get('reservation_id')
    if reservation_id:
        reservation = get_object_or_404(Reservation, id=reservation_id)
        return render(request, 'reservation_success.html', {'reservation': reservation})
    else:
        return redirect('reserve_table')




def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('manage_reservations')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'edit_reservation.html', {'form': form})


def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == "POST":
        reservation.delete()
        return redirect('manage_reservations')
    return render(request, 'confirm_delete.html', {'reservation': reservation})



# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MyUser  # Import your custom user model


def manage_users(request):
    main_admins = MyUser.objects.filter(username='tanvir_shakib')
    customer_users = MyUser.objects.exclude(username='tanvir_shakib').filter(groups__name='Customer')
    staff_users = MyUser.objects.exclude(username='tanvir_shakib').filter(groups__name__in=['Manager', 'Staff', 'Admin'])
    
    # If any user doesn't belong to any of the above groups, classify them as regular users
    regular_users = MyUser.objects.exclude(id__in=main_admins).exclude(id__in=customer_users).exclude(id__in=staff_users)

    context = {
        'main_admins': main_admins,
        'customer_users': customer_users,
        'staff_users': staff_users,
        'regular_users': regular_users,
    }
    return render(request, 'manage_users.html', context)


def edit_user(request, user_id):
    user = get_object_or_404(MyUser, id=user_id)
    if request.method == "POST":
        user.username = request.POST.get('username')
        user.name = request.POST.get('name')
        user.phone_number = request.POST.get('phone')
        new_password = request.POST.get('new_password')
        if new_password:
            user.set_password(new_password)
        user.save()
        return redirect('manage_users')
    return redirect('manage_users')

def delete_user(request, user_id):
    user = get_object_or_404(MyUser, id=user_id)
    if request.method == "POST":
        user.delete()
        return redirect('manage_users')
    return redirect('manage_users')


def add_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = MyUser.objects.create_user(username=username, password=password)
        user.name = name
        user.phone_number = phone
        user.save()
        return redirect('manage_users')
    return redirect('manage_users')




# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Category
from .forms import MenuItemForm, CategoryForm


def manage_menu(request):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.all()

    if request.method == 'POST':
        if 'add_item' in request.POST:
            form = MenuItemForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('manage_menu')
        elif 'add_category' in request.POST:
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                return redirect('manage_menu')
    else:
        form = MenuItemForm()
        category_form = CategoryForm()

    context = {
        'categories': categories,
        'menu_items': menu_items,
        'form': form,
        'category_form': category_form
    }
    return render(request, 'manage_menu.html', context)


def edit_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('manage_menu')
    else:
        form = MenuItemForm(instance=item)

    context = {'form': form, 'item_id': item_id}
    return render(request, 'edit_menu_item.html', context)


def delete_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('manage_menu')

    context = {'item': item}
    return render(request, 'delete_menu_item.html', context)


def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('manage_menu')
    else:
        form = CategoryForm(instance=category)

    context = {'form': form, 'category_id': category_id}
    return render(request, 'edit_category.html', context)


def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('manage_menu')

    context = {'category': category}
    return render(request, 'delete_category.html', context)


