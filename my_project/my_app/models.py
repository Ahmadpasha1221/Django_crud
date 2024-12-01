from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50,null=True,blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    published = models.DateTimeField(auto_now_add=True)