from django.urls import path
from .views import ProductCreateD, ProductCreateDDetail, ListProductD, btn_to_give_an_order, DeleteProduct, ListProductDAll
from . import views

urlpatterns = [
    path('produto/novo', ProductCreateD.as_view(), name='new_productd'),
    path("post/<int:pk>/", ProductCreateDDetail.as_view(), name='post-detail'),
    path("user/<str:username>", ListProductD.as_view(), name='post-user'),
    path("product/<str:username>", ListProductDAll.as_view(), name='list-all-product'),
    path("conceber_pedido/<int:product_id>/", btn_to_give_an_order, name="conceber_pedido" ),
    path("post/<int:pk>/delete", DeleteProduct.as_view(), name='post_delete')
]