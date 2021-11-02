from djongo import models

class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True

class User(TimeStamp):
    name     = models.CharField(max_length = 16)
    email    = models.CharField(max_length = 128)
    password = models.CharField(max_length = 512)
    
    class Meta:
        db_table = 'users'
