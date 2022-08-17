from django.db import models

# Create your models here.

class Carousel(models.Model):
    title       = models.CharField(max_length=100)
    discription      = models.CharField(max_length=100)
    banner_image       = models.ImageField(upload_to='carousel')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title