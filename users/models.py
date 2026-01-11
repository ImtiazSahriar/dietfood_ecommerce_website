from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

#Create your models here.
class SiteLogo(models.Model):
    image = models.ImageField(upload_to="logos/")
    url = models.URLField(max_length=300)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NavOption(models.Model):
    title = models.CharField(max_length=300)
    url= models.URLField(max_length=300)
    order= models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    create_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Button(models.Model):
    icon = models.ImageField(upload_to="button/")
    url = models.URLField(max_length=300)   
    order = models.PositiveIntegerField(default =0)

    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

class HeroSection(models.Model):
    label = models.CharField(max_length=100, blank = True)
    heading = models.CharField(max_length=255)
    description = models.TextField(blank = True)

    background_image = models.ImageField(
        upload_to= 'hero/',
        blank= True,
        null = True
    )

    is_active= models.BooleanField(default=True)
    order = models.PositiveIntegerField(default = 0)

    create_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.heading
    
class HeroButton(models.Model):
    hero = models.ForeignKey(
        HeroSection, on_delete=models.CASCADE, related_name= 'buttons'

    ) 

    text = models.CharField(max_length=100)
    url = models.URLField(max_length=300)

    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.text


class Category(models.Model):
    name= models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    image= models.ImageField(upload_to='categories/', 
                             blank = True,
                             null= True)

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='products'
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    image = models.ImageField(upload_to='products/')
    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_price =models.DecimalField( max_digits=8, decimal_places= 2, blank= True, null =True)

    is_featured= models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_New_Arrival = models.BooleanField(default= True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class ProductImage(models.Model):

    product= models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name= 'images'

    )
    image = models.ImageField(upload_to='products/gallery/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f'image for {self.product.name}'
    

class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete= models.CASCADE, 
        related_name= 'reviews'
    )
    user = models.ForeignKey(
        User, 
        on_delete= models.CASCADE,
        related_name= 'reviews'
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.rating} - {self.product.name}'
    
# class Cart(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete= models.CASCADE,
#         related_name= 'cart'
#     )
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now= True)

class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(is_active=True),
                name='unique_active_cart_per_user'
            )
        ]

    def __str__(self):
        return f"{self.user} - Active: {self.is_active}"



class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} in cart of {self.quantity}'


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status =models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE ,
        related_name='items',
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return  f"{self.product.name} x {self.quantity}"
    




# class Cart(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Cart of {self.user.username}"


# class CartItem(models.Model):
#     class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
#     product_name = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f"{self.product_name} x {self.quantity}"







# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone = models.CharField(max_length=20, blank=True)
#     address = models.TextField(blank=True)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.user.username



