from django.db import models
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User

class PedidoForm(models.Model):
    category_product = [
        ('eletronicos', 'Eletrônicos'),
        ('roupa_feminina', 'Roupa Feminina'),
        ('roupa_masculina', 'Roupa Masculina'),
        ('roupa_infantil', 'Roupa Infantil'),
        ('imoveis', 'Imóveis'),
        ('outro', 'Outro'),
    ]

    name = models.CharField(max_length=100)
    quantity = models.PositiveBigIntegerField()
    category = models.CharField(max_length=50, choices=category_product)
    photo = models.ImageField(upload_to='pedidos/')
    content = models.TextField()
    date_product = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.quantity} unidades)'
    
    def get_absolute_url(self):
        return reverse('pedido-detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['-date_product']


class PedidoDoacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(PedidoForm, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} pediu {self.produto.name}"