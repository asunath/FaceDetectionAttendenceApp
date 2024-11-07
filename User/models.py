from django.db import models

from Admin.models import leaveType
from django.contrib.auth.models import User

# Create your models here.



# USER DATA TABLE
class userprofile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    dob = models.DateField()
    mobile =  models.CharField(max_length=50)
    email = models.EmailField(max_length=50,unique=True)
    doj = models.DateField()
    image = models.ImageField(null=True, blank=True, upload_to="profile_pics/")
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=50)



class userLeave(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    leave_type = models.ForeignKey(leaveType, on_delete=models.CASCADE)
    remaining_leaves = models.IntegerField(default=0)



