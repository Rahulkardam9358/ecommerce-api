from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class AccountManager(BaseUserManager):
    def create_user(self,first_name,email,password,active=True,admin=False,staff=False):
        user=self.model(
            first_name = first_name,
            email = self.normalize_email(email),
            is_active = active,
            admin = admin,
            is_staff=staff
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,first_name,email,password=None):
        user=self.create_user(first_name,email,password,admin=True,staff=True)
        return user

    def create_staff(self,first_name,email,password=None):
        user=self.create_user(first_name,email,password,staff=True)
        return user


class Account(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255,null=True, blank=False)
    last_name = models.CharField(max_length=255, default='')
    is_active=models.BooleanField(default=False)
    admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name']

    objects=AccountManager()
    class Meta:
        db_table = 'account'

    def __str__(self):
        return self.email

    def has_perm(self,perm_list,obj=None):
        return True

    def has_module_perms(self,package_name):
        return True


product_availability = (
    ('Out of Stock', 'Out of Stock'),
    ('Available', 'Available'),
    ('Coming Soon', 'Coming Soon'),
)

class Category(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    image = models.ImageField(upload_to='category')

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    price = models.FloatField()
    description = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product')
    availability = models.CharField(max_length=20,choices=product_availability)
    rating = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.title}'

    def update_rating(self):
        ratings = Review.objects.filter(product__id=self.id)
        n = len(ratings)
        if ratings:
            self.rating = ratings.aggregate(models.Sum('rating'))['rating__sum']//n
        return


class Review(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    rating = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)
        self.product.update_rating()
        return