from django.db import models

from django.contrib.auth.models import User

# Create your models here.



# Leave types and Leave data table
class leaveType(models.Model): 
    name = models.CharField(max_length=50) 
    limit = models.IntegerField(default=0)



class leaveRequests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    type = models.CharField(max_length=50)
    startDate = models.DateField()
    endDate = models.DateField()
    reason = models.CharField(max_length=50)
    status = models.CharField(max_length=50, blank=True, null=True, default="Submitted")