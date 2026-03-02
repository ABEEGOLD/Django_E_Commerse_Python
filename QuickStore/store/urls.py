from django.urls import path, include
from . import views
from rest_framework_nested  import routers



router = routers.DefaultRouter()


router.register("products", views.ProductViewSet, basename="products")
router.register("carts", views.CartViewSet, basename="carts")
router.register("orders", views.OrderViewSet, basename="orders")



product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", views.ReviewViewSet, basename="reviews")


cart_router = routers.NestedDefaultRouter(router,"carts", lookup="cart")
cart_router.register("items", views.CartItemViewSet, basename="carts-items")


urlpatterns = router.urls + product_router.urls + cart_router.urls

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