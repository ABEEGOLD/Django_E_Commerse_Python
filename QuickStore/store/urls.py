from django.urls import path, include
from . import views
from rest_framework_nested  import routers



router = routers.DefaultRouter()


router.register("products", views.ProductViewSet, basename="products")
router.register("carts", views.ProductViewSet, basename="carts")


product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", views.ReviewViewSet, basename="reviews")


cart_router = routers.NestedDefaultRouter(router,"carts", lookup="carts")
cart_router.register("items", views.CartItemViewSet, basename="carts")


urlpatterns = router.urls + product_router.urls

# urlpatterns = [
#
#     path( '', include(router.urls)),
#
#     path( '', include(product_router.urls)),
#
#
#     # path( '<int:pk>/',views.product_detail, name='product_list'),
#
# ]