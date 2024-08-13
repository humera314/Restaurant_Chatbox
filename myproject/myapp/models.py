from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings

class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, name, password=None):
        if not phone_number:
            raise ValueError('The Phone Number is required')
        if not name:
            raise ValueError('The Name is required')
        user = self.model(phone_number=phone_number, name=name)
        user.set_password(password)
        user.username = self.generate_username(name)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, password=None):
        user = self.create_user(phone_number, name, password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def generate_username(self, name):
        username = name.lower().replace(' ', '_')
        if self.model.objects.filter(username=username).exists():
            count = self.model.objects.filter(username__startswith=username).count()
            username = f'{username}_{count+1}'
        return username

class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Add this line

    objects = MyUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.phone_number



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} with total {self.total}"
    


from django.db import models
from django.conf import settings

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    num_of_people = models.IntegerField()
    special_requests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date} at {self.time}"
    



# myapp/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=100, blank=True, null=True)
    special = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    def __str__(self):
        return self.name








    


