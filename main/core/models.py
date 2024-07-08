from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.



class CustomManager(BaseUserManager):
    
    
    def create_user(self, username, email, password=None, **extra_fields):
        
        if not username:
            raise ValueError('Email is required')
        if not email:
            raise ValueError('Email is required')
        if not password:
            raise ValueError('Password is required')
        email = self.normalize_email(email)
        user = self.model(username=username,email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username,email,password=None,**extra_fields):
        
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(username=username,email=email,password=password,**extra_fields)
    
class TodoAppUsers(AbstractUser):
    email = models.EmailField(unique=True,blank=False,null=False)
    username = models.CharField(max_length=100,unique=True,blank=False,null=False)
    bio = models.TextField(blank=True,null=True)
    DOB = models.DateField(blank=True,null=True)
    age = models.PositiveIntegerField(blank=True,null=True)
    objects = CustomManager()
    
    def __str__(self):
        return self.email
