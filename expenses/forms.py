from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Transaction, Item, Category, AccountInfo
# Create your models here.

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = AccountInfo
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'description', 'date', 'item']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'planned', 'received']