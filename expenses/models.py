from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission, BaseUserManager
from django.db import models 
# Create your models here.

class Report(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title

class AccountInfoManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)
    
    

class AccountInfo(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AccountInfoManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    groups = models.ManyToManyField(Group, related_name='accountinfo_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='accountinfo_set', blank=True)

    def __str__(self):
        return self.username
    


class Category(models.Model):   
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    planned = models.FloatField(max_length=15)
    received = models.FloatField(max_length=15)

    def __str__(self):
        return self.name
    

class Transaction(models.Model):        
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateTimeField()
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    

    def __str__(self):
        return self.category