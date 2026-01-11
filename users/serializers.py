from rest_framework import serializers
from .models import *



class SiteLogoSerializers(serializers.ModelSerializer):
    
    class Meta:
       model = SiteLogo
       fields = '__all__'
        

class NavOptionSerializers(serializers.ModelSerializer):
 
    class Meta:
        model = NavOption
        fields = '__all__'



class ButtonSerializers(serializers.ModelSerializer):

    class Meta:
        model = Button
        fields = '__all__'


class heroSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = HeroSection
        fields = '__all__'

class HeroButtonSerializer(serializers.ModelSerializer):

    class Meta:
        model = HeroButton
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    product_slug = serializers.SlugField(source='product.slug', read_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_image', 
                  'product_slug', 'quantity', 'price', 'subtotal']
        read_only_fields = ['price']
    
    def get_subtotal(self, obj):
        return obj.price * obj.quantity
    

    


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'user', 'is_active', 'items', 'total', 
                  'total_items', 'created_at', 'updated_at']
        
    def get_total(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())
    
    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())    


class CartSummarySerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'subtotal', 'total_quantity']
    
    def get_subtotal(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())
    
    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.items.all())


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields =  '__all__' 

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields =  ['id', 'user', 'rating', 'comment', 'created_at']

class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields =  '__all__' 

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0




# class CartSummarySerializer(serializers.ModelSerializer):
#     subtotal = serializers.SerializerMethodField()
#     total_quantity = serializers.SerializerMethodField()

#     class Meta:
#         model = Cart
#         fields =  '__all__' 
#     def get_subtotal(self, obj):
#         return sum(item.price * item.quantity for item in obj.items.all())

#     def get_total_quantity(self, obj):
#         return sum(item.quantity for item in obj.items.all())





# class OrderListSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Order
#         fields =  '__all__' 

# class OrderItemSerializer(serializers.ModelSerializer):
#     product_name = serializers.CharField(source='product.name', read_only=True)

#     class Meta:
#         model = OrderItem
#         feild = '__all__'  



class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 
                  'quantity', 'price', 'subtotal']
    
    def get_subtotal(self, obj):
        return obj.price * obj.quantity
    

class OrderListSerializer(serializers.ModelSerializer):
    total_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'total_amount', 'status', 'created_at', 
                  'is_paid', 'total_items']
    
    def get_total_items(self, obj):
        return obj.items.count()


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_amount', 'status', 
                  'is_paid', 'created_at', 'items']

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_amount', 'status', 'is_paid', 
                  'created_at', 'items', 'total_items']
    
    def get_total_items(self, obj):
        return obj.items.count()




class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['product', 'rating', 'comment'] 
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value





































# class ProductImage(serializers.ModelSerializer):

#     class Meta:
#         models = ProductImage
#         feilds = '__all__'      

