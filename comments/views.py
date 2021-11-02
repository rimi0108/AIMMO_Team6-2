import json
from json.decoder import JSONDecodeError

from django.http.response import JsonResponse
from django.views         import View

from users.decorators import login_decorator
from posts.models     import Post 
from .models          import Comment

class CommentView(View):
    @login_decorator
    def post(self, request, post_id):
        try:
            data    = json.loads(request.body)
            post    = Post.objects.get(id=post_id)
            content = data['content']

            if not content:
                return JsonResponse({'MESSAGE' : 'EMPTY_CONTENT'}, status=400)

            Comment.objects.create(
                user    = request.user,
                post    = post,
                content = content
            )
            return JsonResponse({'MESSAGE' : 'COMMENT_CREATE'}, status=201)
        
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({'MESSAGE' : 'JSON_DECODE_ERROR'}, status=400)
        
    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id)

        result = [{
            'user'       : comment.user.name,
            'content'    : comment.content,
            'created_at' : comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for comment in comments]

        return JsonResponse({"RESULT" : result}, status = 200)
    
    @login_decorator
    def put(self, request, post_id, comment_id):
        try:
            data    = json.loads(request.body)
            content = data['content']

            if not Post.objects.filter(id = post_id).exists():
                return JsonResponse({"MESSAGE" : "DOES_NOT_EXIST_POST"}, status = 404)
            if not Comment.objects.filter(id=comment_id, post_id=post_id).exists():
                return JsonResponse({"MESSAGE" : "DOES_NOT_EXIST_COMMENT"}, status = 404)
            if Comment.objects.get(id = comment_id).user.id != request.user.id:
                return JsonResponse({"MESSAGE" : "NO_PERMISSION"}, status = 401)

            Comment.objects.filter(id = comment_id, post_id=post_id, user_id=request.user.id).update(
                content = content
            )

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE_ERROR'}, status = 400)
        
    @login_decorator
    def delete(self, request, post_id, comment_id):
        
        if not Post.objects.filter(id = post_id).exists():
            return JsonResponse({"MESSAGE" : "DOES_NOT_EXIST_POST"}, status = 404)
        
        if not Comment.objects.filter(id=comment_id, post_id=post_id).exists():
            return JsonResponse({"MESSAGE" : "DOES_NOT_EXIST_COMMENT"}, status = 404)
        
        if Comment.objects.get(id = comment_id).user.id != request.user.id:
            return JsonResponse({"MESSAGE" : "NO_PERMISSION"}, status = 401)

        Comment.objects.filter(id = comment_id, post_id=post_id, user_id=request.user.id).delete()

        return JsonResponse({"MESSAGE" : "DELETED"}, status = 200)

class NestedCommentView(View):
    @login_decorator
    def post(self, request, comment_id):
        data = json.loads(request.body)

        if not Comment.objects.filter(id=comment_id).exists():
            return JsonResponse({'MESSAGE':'DOES_NOT_EXIST_COMMENT'}, status=404)
        
        if not Comment.objects.filter(id=comment_id, nested_comment__isnull=True).exists():
            return JsonResponse({'MESSAGE':'DOES_NOT_LEAVE_NESTED_COMMENT'})
        
        post_id = Comment.objects.get(id=comment_id).post_id

        Comment.objects.create(
            content            = data['content'],
            post_id            = post_id,
            nested_comment_id  = comment_id,
            user               = request.user
        )
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)
    
    def get(self, request, comment_id):
        comments = Comment.objects.filter(nested_comment_id=comment_id)

        result = [{
            'user'       : comment.user.name,
            'content'    : comment.content,
            'created_at' : comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for comment in comments]

        return JsonResponse({"RESULT" : result}, status = 200)

    @login_decorator
    def put(self, request, comment_id, nested_comment_id):
        try:
            data    = json.loads(request.body)
            content = data['content']

            if not Comment.objects.filter(id=nested_comment_id, nested_comment_id=comment_id).exists():
                return JsonResponse({"MESSAGE" : "DOES_NOT_EXIST_NESTED_COMMENT"}, status = 404)
           
            if Comment.objects.get(id=nested_comment_id, nested_comment_id=comment_id).user.id != request.user.id:
                return JsonResponse({"MESSAGE" : "NO_PERMISSION"}, status = 401)

            Comment.objects.filter(id=nested_comment_id, nested_comment_id=comment_id, user_id=request.user.id).update(
                content = content
            )

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE_ERROR'}, status = 400)

    @login_decorator
    def delete(self, request, comment_id, nested_comment_id):
        
        if not Comment.objects.filter(id=nested_comment_id, nested_comment_id=comment_id).exists():
            return JsonResponse({"MESSAGE" : "DOES_NOT_EXIST_NESTED_COMMENT"}, status = 404)
           
        if Comment.objects.get(id=nested_comment_id, nested_comment_id=comment_id).user.id != request.user.id:
            return JsonResponse({"MESSAGE" : "NO_PERMISSION"}, status = 401)

        Comment.objects.filter(id=nested_comment_id, nested_comment_id=comment_id, user_id=request.user.id).delete()

        return JsonResponse({"MESSAGE" : "DELETED"}, status = 200)
        