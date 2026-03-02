from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets, status
from .models import Product, Review, Cart, CartItem, Order
from .serializers import ProductSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, \
    UpdateCartItemSerializer, OrderSerializer, CreateOrderSerializer
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin





class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer


    def get_queryset(self):
        return Review.objects.filter(product=self.kwargs['product_pk'])


    def get_serializer_context(self):
        return {"product_id": self.kwargs['product_pk']}



class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer



class CartItemViewSet(viewsets.ModelViewSet):

    http_method_names = ['get','post','patch','delete']


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart=self.kwargs['cart_pk'])


    def get_serializer_context(self):
        return {"cart_id": self.kwargs['cart_pk']}


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer


    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        Order = serializer.save()
        serializer = OrderSerializer(Order)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


    # Create your views here.
    # @api_view(['GET'])
    # def product_list(request):
    #    products = Product.objects.all()
    #    serializer = ProductSerializer(products, many=True)
    #    return Response(serializer.data, status=status.HTTP_200_OK)



    # def create_product(request):
    #     data = ProductSerializer(data=request.data)
    #     data.is_valid(raise_exception=True)
    #     data.save()
    #     return Response(data.data, status=status.HTTP_201_CREATED)


# # this can be implemented without the first instansiate method
# class ProductView(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


# @api_view()
# def product_detail(request, pk):
#       product = get_object_or_404(Product, pk=pk)
#       serializer = ProductSerializer(product)
#       return Response(serializer.data, status=status.HTTP_200_OK)







