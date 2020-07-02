from django.urls import path
from .views import ProductViewSet, CSVProductViewSet



app_name = "products"

urlpatterns = [
    # product list
    path('', ProductViewSet.as_view(),name='product_list'),
    path('product_list_in_csv/', CSVProductViewSet.as_view(),name='product_csv'),



]
