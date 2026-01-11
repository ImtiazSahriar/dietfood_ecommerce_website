from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status 
from .pagination import *
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
# Create your views here.
class SiteLogoAPIView(APIView):

    def get(self, request):
        logos = SiteLogo.objects.filter(is_active=True).order_by('-updated_at').first()
        serializer = SiteLogoSerializers(logos)   
        return Response(serializer.data, status=status.HTTP_200_OK)

class NavOptionAPIVIEW(APIView):

    def get(self, request):
        nav =  NavOption.objects.filter(is_active = True).order_by('updated_at').first()
        serializers = NavOptionSerializers(nav)
        return Response(serializers.data, status=status.HTTP_200_OK)

class ButtonAPIVIEW(APIView):

    def get(self, request):
        button = Button.objects.filter(is_active = True).order_by('updated_at').first()
        serializers= ButtonSerializers(button)
        return Response(serializers.data, status=status.HTTP_200_OK)



class HomeCategoryAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(is_active=True)[:4]
    
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
 

class HomeProductAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(is_active=True).order_by('-created_at')[:4]
    
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

class HomeNewArrivalAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    

    def get_queryset(self):
        return (
            Product.objects
            .filter(is_active=True)
            .order_by('-created_at')[:3]
        )
    
class NewArrivalListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = NewArrivalPagination

    def get_queryset(self):
        return Product.objects.filter(
            is_active=True
        ).order_by('-created_at')

class NewsletterSubscriberAPIVIEW(APIView):

    def post(self, request):
        serializers = NewsletterSubscriberSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)         
     


# class NewsletterSubscriberCreateAPIView(generics.CreateAPIView):
#     serializer_class = NewsletterSubscriberSerializer

class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            is_active=True
        )
        serializer = CartSerializer(cart)
        return Response(serializer.data)



class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id, is_active=True)

        cart, _ = Cart.objects.get_or_create(
            user=request.user,
            is_active=True
        )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                'quantity': quantity,
                'price': product.discount_price or product.price
            }
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class UpdateCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, item_id):
        quantity = int(request.data.get('quantity'))

        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user,
            cart__is_active=True
        )

        if quantity <= 0:
            cart_item.delete()
            return Response(
                {"detail": "Item removed"},
                status=status.HTTP_204_NO_CONTENT
            )

        cart_item.quantity = quantity
        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)




class RemoveCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user,
            cart__is_active=True
        )

        cart_item.delete()
        return Response(
            {"detail": "Item removed from cart"},
            status=status.HTTP_204_NO_CONTENT
        )




class PlaceOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        # 1️⃣ Get active cart
        try:
            cart = Cart.objects.get(user=request.user, is_active=True)
        except Cart.DoesNotExist:
            return Response(
                {"detail": "No active cart found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_items = cart.items.all()

        # 2️⃣ Check empty cart
        if not cart_items.exists():
            return Response(
                {"detail": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3️⃣ Create order (temporary total 0)
        order = Order.objects.create(
            user=request.user,
            total_amount=0,
            status='pending'
        )

        total_amount = 0

        # 4️⃣ Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price
            )
            total_amount += item.price * item.quantity

        # 5️⃣ Update total amount
        order.total_amount = total_amount
        order.save()

        # 6️⃣ Deactivate cart
        cart.is_active = False
        cart.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ProductDetailAPIView(APIView):

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug, is_active=True)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)




class CartSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_object_or_404(
            Cart,
            user=request.user,
            is_active=True
        )
        serializer = CartSummarySerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)





class UserOrderListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).order_by('-created_at')


#order detail
class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(
            Order,
            id=order_id,
            user=request.user
        )
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)




class ReviewCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReviewCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data['product']

        # Check if already reviewed
        if Review.objects.filter(user=request.user, product=product).exists():
            return Response(
                {"detail": "You have already reviewed this product"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        has_purchased = OrderItem.objects.filter(
            order__user=request.user,
            product=product,
            order__status='delivered'
        ).exists()

        if not has_purchased:
            return Response(
                {"detail": "You must purchase this product to review"},
                status=status.HTTP_403_FORBIDDEN
            )
        # user manually set 
        Review.objects.create(
            user=request.user,
            product=product,
            rating=serializer.validated_data['rating'],
            comment=serializer.validated_data.get('comment', '')
        )

        return Response(
            {"detail": "Review submitted successfully"},
            status=status.HTTP_201_CREATED
        )




# class HeroSectionAPIVIEW(APIView):

#     def get(self, request):
#         hero = HeroSection.objects.filter(is_active = True).order_by('updated_at').first()
#         serializers = heroSectionSerializer(hero)
#         return Response(serializers.data, status=status.HTTP_200_OK)
    

# class HeroButtonAPIVIEW(APIView):

#     def get(self, request, hero_id):
#         buttons = HeroButton.objects.filter(hero_id= hero_id)
#         serializers = HeroButtonSerializer(buttons, many =True)
#         return Response(serializers.data, status=status.HTTP_200_OK)    
    
# class CategoryAPIVIEW(APIView):

#     def get(self, request):
#         category = Category.objects.filter(is_active = True)
#         serializer = CategorySerializer(category, many = True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class ProductAPIVIEW(APIView):

#      def get(self, request):
#          product = Product.objects.filter(is_active = True)
#          serializers = Product(product, many = True)
#          return Response(serializers.data, status=status.HTTP_200_OK)
    
# class NewsletterSubscriberAPIVIEW(APIView):

#     def post(self, request):
#         serializers = NewsletterSubscriber(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data, status=status.HTTP_201_CREATED)
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)         
    
# class ReviewAPIVIEW(APIView):   

#     def post(self, request):
#         serializers = Review(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data, status=status.HTTP_201_CREATED)
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 
    
# class CartAPIVIEW(APIView):

#     def get(self, request):
#         cart = Cart.objects.all()
#         serializers = Cart(cart, many = True)
#         return Response(serializers.data, status=status.HTTP_200_OK)
    
# class CartItemAPIVIEW(APIView):

#     def get(self, request):
#         cartitem = CartItem.objects.all()
#         serializers = CartItem(cartitem, many = True)
#         return Response(serializers.data, status=status.HTTP_200_OK)
    

# class orderAPIVIEW(APIView):

#     def get(self, request):
#         order_instance = Order.objects.all()
#         serializers = Order(order_instance, many = True)
#         return Response(serializers.data, status=status.HTTP_200_OK)
    
# class OrderItemAPIVIEW(APIView):    
#     def get(self, request):
#         orderitem = OrderItem.objects.all()
#         serializers = OrderItem(orderitem, many = True)
#         return Response(serializers.data, status=status.HTTP_200_OK)
    









#My Orders API (User order history)

# class MyOrdersAPIView(ListAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)


#Order Detail API (Single order)
# class OrderDetailAPIView(RetrieveAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)





