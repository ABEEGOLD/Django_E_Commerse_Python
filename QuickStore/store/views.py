from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets
from .models import Product, Review, Cart
from .serializers import ProductSerializer, ReviewSerializer, cartSerializer, CartItemSerializer
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin





class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer


    def get_queryset(self):
        return Review.objects.filter(product=self.kwargs['product_pk'])


    def get_serializer_context(self):
        return {"product_id": self.kwargs['product_pk']}



class CartViewSet(CreateModelMixin,RetrieveModelMixin,GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = cartSerializer



class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer


    def get_queryset(self):
        return Cart.objects.filter(product=self.kwargs['cart_pk'])






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







