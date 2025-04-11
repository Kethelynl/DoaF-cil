from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Verifique se a imagem existe antes de tentar abri-la
        if os.path.exists(self.image.path):
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
        else:
            print(f"Imagem padrão não encontrada: {self.image.path}")

class UserAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    cidade = models.CharField(max_length=255)
    estado = models.CharField(max_length=2)
    codigo = models.CharField(max_length=9)
    latitude = models.FloatField(null=True, blank=True)  # Nova coluna
    longitude = models.FloatField(null=True, blank=True)  # Nova coluna

    def __str__(self):
        return f'{self.rua}, {self.numero}, {self.cidade}/{self.estado}'