#models.py
from django.db import models

class Product(models.Model):
    id=models.AutoField(primary_key=True)
    predict = models.CharField(max_length=70)
    image = models.ImageField(default="media/default.jpg", upload_to="uploads")
    def __str__(self):
	    return self.predict

