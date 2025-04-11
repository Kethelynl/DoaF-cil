from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class ProductD(models.Model):
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
    photo = models.ImageField(upload_to='produtos/')
    content = models.CharField(max_length=300)
    date_product = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.quantity} unidades)'
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['-date_product']
