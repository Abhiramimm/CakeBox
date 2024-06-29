from django.contrib import admin

from kart.models import Category,Flavour,Occasion,Size,Tag,Cake,CakeVariant

# Register your models here.

admin.site.register(Category)

admin.site.register(Flavour)

admin.site.register(Occasion)

admin.site.register(Size)

admin.site.register(Tag)

admin.site.register(Cake)

admin.site.register(CakeVariant)

