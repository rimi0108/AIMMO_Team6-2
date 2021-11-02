from django.urls import path

from .views import CommentView

urlpatterns = [
    path('<int:post_id>/comment', CommentView.as_view()),
    path('<int:post_id>/comments', CommentView.as_view()),
    path('<int:post_id>/comment/<int:comment_id>', CommentView.as_view()),
    ]