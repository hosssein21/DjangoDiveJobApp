from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from .validators import validate_iranian_phone_number

class UserTypeChoices(models.IntegerChoices):
    
    admin=1, 'admin'
    candidate=2 ,'candidate'
    employer=3 , 'employer'
    

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    type=models.IntegerField(choices=UserTypeChoices.choices,default=UserTypeChoices.candidate)
    
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    
class CandidateProfile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    first_name =models.CharField(max_length=255)
    last_name =models.CharField(max_length=255)
    age = models.SmallIntegerField(null=True,blank=True)
    city= models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11,validators=[validate_iranian_phone_number])
    
    image = models.ImageField(upload_to="CandidateProfile/")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def get_fullname(self):
        if self.first_name or self.last_name:
            return self.first_name + " " + self.last_name
        return "کاربر جدید"
    
    
@receiver(post_save, sender=User)
def create_candidate_profile(sender, instance, created, **kwargs):
    if created and instance.type==2:
        CandidateProfile.objects.create(user=instance)
    
    
class EmployerProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    company_name =models.CharField(max_length=255)
    city= models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11)
    description=models.TextField()
    
    image = models.ImageField(upload_to="EmployerProfile/")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    
@receiver(post_save,sender=User) 
def create_employer_profile(sender, instance, created, **kwargs):
        if created and instance.type==3:
            EmployerProfile.objects.create(user=instance)
    
    
    
    
