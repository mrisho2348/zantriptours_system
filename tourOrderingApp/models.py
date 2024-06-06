from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
        
class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Tourist"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)
    is_active = models.BooleanField(default=True)

    # Provide unique related_name for groups and user_permissions fields
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set'  # Use a unique related_name
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set'  # Use a unique related_name
    )

    objects = CustomUserManager()
    

class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()  
    def __str__(self):
        return self.admin.username  
    
class Country(models.Model):
    name = models.CharField(max_length=100)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    objects = models.Manager()
    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name       


    
class ContactRequest(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    objects = models.Manager()
    
    def __str__(self):
        return self.name   
    
class About(models.Model):    
    content = models.TextField()   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    objects = models.Manager()
    
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    image = models.ImageField(upload_to='feedback_images/', null=True, blank=True)  # Image field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    objects = models.Manager()
    
    def __str__(self):
        return self.name
    
    
class Hotel(models.Model):
    name = models.CharField(max_length=200,unique=True)
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description =models.TextField()
    image = models.ImageField(upload_to='images/')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    objects = models.Manager()
    def __str__(self):
        return self.name
    
class Transport(models.Model):
    name = models.CharField(max_length=200,unique=True)
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description =models.TextField()
    image = models.ImageField(upload_to='Transport_images/')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    objects = models.Manager()
    def __str__(self):
        return self.name
    
class HotelBooking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)    
    phone_number = models.CharField(max_length=20, blank=True, null=True)  
    passport_number = models.CharField(max_length=20, blank=True, null=True)   
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True) 
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    booking_date = models.DateTimeField(default=timezone.now)    
    def __str__(self):
        return f"{self.customer_name} - {self.hotel.name}"     
    
class TransportBooking(models.Model):
    transport_service = models.ForeignKey(Transport, on_delete=models.CASCADE, blank=True, null=True)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)    
    phone_number = models.CharField(max_length=20, blank=True, null=True)  
    passport_number = models.CharField(max_length=20, blank=True, null=True)   
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True) 
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    booking_date = models.DateTimeField(default=timezone.now)    
    def __str__(self):
        return f"{self.customer_name} - {self.transport_service.name}"     
    

    
class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    website = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    objects = models.Manager()

    def __str__(self):
        return self.name



class Transportation(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    availability = models.CharField(max_length=50)
    image = models.ImageField(upload_to='transportation_images/', null=True, blank=True)  # ImageField added
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.name



    
            
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:  # HOD
            AdminHOD.objects.create(admin=instance)

   
            
 
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
