from django.contrib import admin
from .models import Transaction, AccountInfo, Category, Item
# Register your models here.

admin.site.register(Transaction)
admin.site.register(AccountInfo)
admin.site.register(Category)
admin.site.register(Item)