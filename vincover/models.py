from django.db import models

# Create your models here.

class User(models.Model):
    id=models.BigIntegerField(primary_key=True)
    name=models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    class Meta:
        db_table='vin_user'
