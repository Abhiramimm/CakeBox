from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save


# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=200, unique=True)

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    
    def __str__(self):

        return self.name

class Flavour(models.Model):

    name = models.CharField(max_length=200, unique=True)

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    
    def __str__(self):

        return self.name

class Occasion(models.Model):

    name = models.CharField(max_length=200, unique=True)

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    
    def __str__(self):

        return self.name
    
class Size(models.Model):

    name = models.CharField(max_length=200, unique=True)

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    
    def __str__(self):

        return self.name

class Tag(models.Model):

    name = models.CharField(max_length=200, unique=True)

    def __str__(self):

        return self.name

class Cake(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField(null=True, blank=True)

    category_object = models.ForeignKey(Category,on_delete=models.CASCADE)

    size_object=models.ManyToManyField(Size)

    flavour_object = models.ManyToManyField(Flavour)

    occasion_object=models.ForeignKey(Occasion,on_delete=models.CASCADE)

    tag_object=models.ManyToManyField(Tag)

    image = models.ImageField(upload_to='product_images', null=True, blank=True, default='product_images/default.jpg')

    created_date = models.DateTimeField(auto_now_add=True)
    
    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    
    def __str__(self):

        return self.title

class CakeVariant(models.Model):

    cake_object=models.ForeignKey(Cake,on_delete=models.CASCADE)

    size_object=models.ForeignKey(Size,on_delete=models.CASCADE)

    price=models.PositiveIntegerField()
    
class Basket(models.Model):

    owner = models.OneToOneField(User, on_delete=models.CASCADE,related_name="cart")

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    
    def __str__(self):

        return self.owner.username
    
    @property
    def cart_item_count(self):

        return self.cartitems.filter(is_order_placed=False).count()
    
    @property
    def cart_total(self):

        basket_items=self.cartitems.filter(is_order_placed=False)

        total_price=0

        if basket_items:

            for bi in basket_items:

                total_price+=bi.total_amount
                
        return total_price
  
class BasketItem(models.Model):

    basket_object = models.ForeignKey(Basket, on_delete=models.CASCADE,related_name="cartitems")

    size_object=models.ForeignKey(Size,on_delete=models.CASCADE,null=True)

    cakevariant_object=models.ForeignKey(CakeVariant,on_delete=models.CASCADE,null=True)

    qty=models.PositiveIntegerField(default=1)

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    is_order_placed=models.BooleanField(default=False)

    

    @property
    def total_amount(self):

        return self.cakevariant_object.price*self.qty

class Order(models.Model):

    user_object = models.ForeignKey(
                                        User,
                                        on_delete=models.CASCADE, 
                                        related_name='myorders'
                                    )

    basket_item_objects = models.ManyToManyField(BasketItem)

    message = models.TextField(null=True, blank=True)

    delivery_address = models.CharField(max_length=250)

    phone = models.CharField(max_length=12)

    pin=models.CharField(max_length=10,null=True)

    email = models.CharField(max_length=100)

    pay_options = (
        ('online', 'online'),
        ('cod', 'cod')
    )

    payment_mode = models.CharField(
                                        max_length=100, 
                                        choices=pay_options, 
                                        default='cod'
                                    )

    order_id = models.CharField(max_length=200, null=True)

    is_paid = models.BooleanField(default=False)

    order_status = (
        ('order_confirmed', 'Order confirmed'),
        ('dispatched', 'Dispatched'),
        ('in_transit', 'In transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),

    )

    status = models.CharField(
                                max_length=200, 
                                choices=order_status, 
                                default='order_confirmed'
                            )

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def sub_total(self):

        baket_items=self.basket_item_objects.all()

        total=0

        if baket_items:

            for bi in baket_items:
                
                total+=bi.total_amount

        return total

    

def create_basket(sender,instance,created,**kwargs):

    if created:

        Basket.objects.create(owner=instance)

post_save.connect(sender=User,receiver=create_basket)



def create_basket(sender,instance,created,**kwargs):

    if created:

        Basket.objects.create(owner=instance)

post_save.connect(sender=User,receiver=create_basket)
    











