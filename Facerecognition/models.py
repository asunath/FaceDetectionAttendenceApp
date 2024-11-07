from django.db import models

from Admin.models import User

# Create your models here.



# Attendance table
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()