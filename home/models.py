from django.db import models

# Create your models here.
class uploadfile(models.Model):
    f_name = models.CharField(max_length=255)
    myfiles = models.FileField(upload_to="")
    campus_name = models.CharField(max_length=100,null=True)
    
    def __str__(self):
        return self.f_name