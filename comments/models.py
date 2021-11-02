from djongo import models
from users.models import TimeStamp, User
from posts.models import Post


class Comment(TimeStamp):
  content        = models.CharField(max_length = 500)
  user           = models.ForeignKey(User, on_delete = models.CASCADE)
  nested_comment = models.ForeignKey('self', on_delete = models.CASCADE, null = True)
  post           = models.ForeignKey(Post, on_delete = models.CASCADE)

  class Meta:
    db_table = 'comments'