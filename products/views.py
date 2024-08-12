# products/views.py

from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .utils import read_product_data, write_product_data
import os

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')  # Redirect to the product list after login
    else:
        form = AuthenticationForm()
    
    return render(request, 'products/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')  # Redirect to the product list after registration
    else:
        form = UserCreationForm()
    
    return render(request, 'products/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

@login_required
def product_list_view(request):
    query = request.GET.get('q')  # Get the search query from the request
    directory = os.path.join(os.path.dirname(__file__), 'product_files')
    product_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    products = [os.path.splitext(f)[0].replace('_', ' ') for f in product_files]

    if query:
        products = [product for product in products if query.lower() in product.lower()]

    context = {'products': products}
    return render(request, 'products/product_list.html', context)


@login_required
def product_view(request, product_file):
    directory = os.path.join(os.path.dirname(__file__), 'product_files')
    file_path = os.path.join(directory, f"{product_file}.txt")

    if not os.path.exists(file_path):
        raise Http404("Product file not found")

    product_name, stock_price, market_value, logs = read_product_data(file_path)

    if request.method == 'POST':
        new_market_value = request.POST.get('market_value')
        write_product_data(file_path, new_market_value, request.user.username)
        return redirect('product_view', product_file=product_file)

    context = {
        'product_name': product_name,
        'stock_price': stock_price,
        'market_value': market_value,
        'logs': logs
    }
    return render(request, 'products/product.html', context)


