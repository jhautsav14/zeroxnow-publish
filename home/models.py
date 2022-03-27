from django.db import models

# Create your models here.
class uploadfile(models.Model):
    f_name = models.CharField(max_length=255)
    myfiles = models.FileField(upload_to="")
    campus_name = models.CharField(max_length=100,null=True)
    
    def __str__(self):
        return self.f_name

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length= 90)
    campus = models.CharField(max_length=500, null=True)
    paymentorder_id = models.CharField(max_length=111,null=True)
    
    