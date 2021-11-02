from django.db.models.deletion import CASCADE

from users.models import User,TimeStamp
from djongo       import models

class Post(TimeStamp):
    author   = models.CharField(max_length = 16)
    title    = models.CharField(max_length = 200)
    content  = models.TextField()
    counting = models.IntegerField()
    user     = models.ForeignKey(User, on_delete = models.CASCADE)
    category = models.ForeignKey('category', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'posts'

class Category(models.Model):
    name = models.CharField(max_length = 16)
    
    class Meta:
        db_table = 'categories'