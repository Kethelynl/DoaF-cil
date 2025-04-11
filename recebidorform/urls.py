from django.urls import path
from .views import PedidoCreateD, PedidoCreateDetail, ListPedido, request_donation, DeletePedido, ListPedidoAll
from . import views

urlpatterns = [
    path('pedido/novo', PedidoCreateD.as_view(), name='new_gif'),
    path("pedido/<int:pk>/", PedidoCreateDetail.as_view(), name='pedido-detail'),
    path("user/<str:username>", ListPedido.as_view(), name='post-user'),
    path("pedidos/<str:username>", ListPedidoAll.as_view(), name='list-all'),
    path("pedido/<int:pk>/delete", DeletePedido.as_view(), name='pedido_delete'),
    path("solicitar_doação/<int:product_id>/", request_donation, name='solicitar_doacao'),
]