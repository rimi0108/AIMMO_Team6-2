from django.urls import path

from .views import CommentView, NestedCommentView

urlpatterns = [
    path('<int:post_id>/comment', CommentView.as_view()),
    path('<int:post_id>/comments', CommentView.as_view()),
    path('<int:post_id>/comment/<int:comment_id>', CommentView.as_view()),
    path('comment/<int:comment_id>', NestedCommentView.as_view()),
    path('comment/<int:comment_id>/<int:nested_comment_id>', NestedCommentView.as_view()),
    ]