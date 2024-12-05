from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum
from .models import Transaction, Category, AccountInfo, Item
from .forms import RegistrationForm, TransactionForm, CategoryForm, ItemForm, LoginForm
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            print(f'User: {user}')

            if user is not None:
                login(request, user)
                messages.success(request, 'Login Successful, Welcome!')
                return redirect('expenses:category')
            else:
                messages.error(request, 'Invalid login. Please try again.')
        else:
            messages.error(request, 'Invalid form submission. Please check your input.')
    else:
        form = LoginForm()

    return render(request, 'budget/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout is successful Thanks for using Budgetly')
    return redirect('budget/login.html')

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            if AccountInfo.objects.filter(username=username).exists() or AccountInfo.objects.filter(email=email).exists():
                messages.error(request, 'Username or email already exists.')
            else:
                
                account_info = AccountInfo(username=username, email=email)
                
                account_info.set_password(form.cleaned_data.get('password1'))
                account_info.save()

                messages.success(request, f'Account successfully created. Welcome, {username}.')
                return redirect('expenses:profile')
        else:
            print('Form is invalid:', form.errors)
    else:
        form = RegistrationForm()

    return render(request, 'budget/Register.html', {'form': form})

def profile_view(request):
    return render(request, 'budget/profile.html')

def add_category_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
         form.save()
        return redirect('expenses:category')    
    else:
        form = CategoryForm()
    return render(request, 'budget/addcategory.html', {'form': form})

def add_item_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expenses:category')
        else:
            return render(request, 'budget/additem.html', {'form': form})
    else:
        form = ItemForm()
    return render(request, 'budget/additem.html', {'form': form})


def edit_item_view(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('expenses:category')
        else:
            return render(request, 'budget/additem.html', {'form': form})
    else:
        form = ItemForm(instance=item) 
    return render(request, 'budget/additem.html', {'form': form})

def add_transaction_view(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('expenses:transactions')  
    else:
        form = TransactionForm()
    return render(request, 'budget/addtransaction.html', {'form': form})

def category_view(request):
    categories = Category.objects.filter()
    items = Item.objects.filter()
    return render(request, 'budget/category.html', {'categories': categories, 'items': items})


def edit_category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('expenses:category') 
    else:
        form = CategoryForm(instance=category)
    return render(request, 'budget/editcategory.html', {'form': form, 'category': category})

def edit_transaction_view(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('expenses:transactions') 
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'budget/edittransaction.html', {'form': form, 'transaction': transaction})

def edit_item_view(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('expenses:category')  # Adjust the redirect URL as needed
    else:
        form = ItemForm(instance=item)

    return render(request, 'budget/edititem.html', {'form': form, 'item': item})

def reports_view(request):
    
    transaction_total = Transaction.objects.aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0
    categories_total = Category.objects.count()
    items_total = Item.objects.count()

    return render(request, 'budget/reports.html', {
        'transaction_total': transaction_total,
        'categories_total': categories_total,
        'items_total': items_total,
    })


def transactions_view(request):
    transactions = Transaction.objects.filter()
    return render(request, 'budget/transactions.html', {'transactions': transactions})



