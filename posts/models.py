from django.db.models.deletion import CASCADE

from users.models import User,TimeStamp
from djongo       import models

class Post(TimeStamp):
    author   = models.CharField(max_length = 16)
    title    = models.CharField(max_length = 200)
    content  = models.TextField()
    counting = models.IntegerField(default=0)
    user     = models.ForeignKey(User, on_delete = models.CASCADE)
    category = models.ForeignKey('category', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'posts'

class Category(models.Model):
    name = models.CharField(max_length = 16)
    
    class Meta:
        db_table = 'categories'

class Saveip(models.Model):
    access_ip = models.CharField(max_length = 50)
    post      = models.ForeignKey('post', on_delete=models.CASCADE)

    class Meta:
        db_table = 'ips'