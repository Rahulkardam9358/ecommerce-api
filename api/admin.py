from django.contrib import admin
from api.models import Account, Product, Category, Review

# Register your models here.
admin.site.register(Account)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Review)
