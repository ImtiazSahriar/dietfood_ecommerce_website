from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib import admin


@admin.register(SiteLogo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "url", "is_active", "created_at", "updated_at")


@admin.register(NavOption)
class NavOptionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "url", "order", "is_active", "create_at", "updated_at")
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)

@admin.register(Button)
class ButtonAdmin(admin.ModelAdmin):
    list_display = ('id', "icon", "url",'order', "is_active", 'create_at', 'updated_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'heading', 'description', 'order', 'is_active', 'create_at', 'updated_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)


@admin.register(HeroButton)
class HeroButtonAdmin(admin.ModelAdmin):
    list_display = ('id', 'hero', 'text', 'url', 'is_primary', 'order', 'is_active')
    list_editable = ('order', 'is_active', 'is_primary')
    list_filter = ('is_active', 'is_primary', 'hero')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display= ('id','name', 'is_active','order', 'created_at', 'updated_at')

    list_editable = ('is_active', 'order')
    
    search_fields = ('name',)
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
# class CategoryAdmin(admin.ModelAdmin):
#     list_display= ('id', 'slug', 'name', 'created_at', 'updated_at')

#     list_editable = ('is_active', 'order')
    
#     search_fields = ('name',)
#     list_filter = ('is_active',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'is_active', 'created_at', 'updated_at')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image', 'is_primary')
    list_editable = ('is_primary',)
    list_filter = ('is_primary', 'product')
    search_fields = ('product__name',)

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'subscribed_at')  

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rating', 'comment', 'created_at')      

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','is_active', 'created_at', 'updated_at')  

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'price')    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount','status','is_paid', 'created_at')
    list_editable = ('status', 'is_paid')
    list_filter = ('status',)
    search_fields = ('user__username',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')









# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ("name", "slug", "created_at")
#     prepopulated_fields = {"slug": ("name",)}

# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ("user", "created_at")

# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ("cart", "quantity")

# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ("user", "phone", "created_at")




  