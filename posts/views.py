import json

from django.http.response import JsonResponse
from django.views         import View
from django.db.models     import Q

from users.decorators import login_decorator
from .models          import Post, Category


class PostView(View):
    @login_decorator
    def post(self, request):
        try:
            data     = json.loads(request.body)
            user     = request.user
            category = Category.objects.get(name = data['category'])
            title    = data['title']
            content  = data['content']

            post = Post.objects.create(
                author   = user.name,
                title    = title,
                content  = content,
                category = category,
                user     = user
            )

            result = {
                'author'     : post.author,
                'title'      : post.title,
                'content'    : post.content,
                'category'   : post.category.name,
                'created_at' : post.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }

            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : result},status = 201)
        
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE_ERROR'}, status = 400)
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)

    def get(self,request,post_id):
        if not Post.objects.filter(id = post_id).exists():
            return JsonResponse({'MESSAGE' : 'DOSE_NOT_EXIST_POST'}, status = 404)

        post = Post.objects.get(id = post_id)

        result = {
                'author'     : post.author,
                'title'      : post.title,
                'content'    : post.content,
                'created_at' : post.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

        return JsonResponse({"RESULT" : result}, status = 200)
    
    @login_decorator
    def delete(self, request, post_id):
        if not Post.objects.filter(id = post_id).exists():
            return JsonResponse({"MESSAGE" : "DOSE_NOT_EXIST_POST"}, status = 404)
        if Post.objects.get(id = post_id).user.id != request.user.id:
            return JsonResponse({"MESSAGE" : "NO_PERMISSION"}, status = 403)

        Post.objects.filter(id = post_id).delete()

        return JsonResponse({"MESSAGE" : "DELETED"}, status = 200)

    @login_decorator
    def put(self, request, post_id):
        try:
            data    = json.loads(request.body)
            title   = data['title']
            content = data['content']

            if not Post.objects.filter(id = post_id).exists():
                return JsonResponse({"MESSAGE" : "DOSE_NOT_EXIST_POST"}, status = 404)
            if Post.objects.get(id = post_id).user.id != request.user.id:
                return JsonResponse({"MESSAGE" : "NO_PERMISSION"}, status = 401)

            post = Post.objects.filter(id = post_id).update(
                title   = title,
                content = content
            )

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE_ERROR'}, status = 400)

class PostListView(View):
    def get(self,request):
        try:
            offset   = int(request.GET.get('offset', 0))
            limit    = int(request.GET.get('limit', 5))
            category = request.GET.get('category')
            search   = request.GET.get('search', None)
            q        = Q()

            if category:
                q &= Q(category__id = category)

            if search:
                q &= Q(title__icontains = search)
                
            posts = Post.objects.filter(q).select_related('category')[offset:offset+limit]
            count = len(posts)
            
            result = [{
                'author'     : post.user.name,
                'title'      : post.title,
                'content'    : post.content,
                'category'   : post.category.name,
                'created_at' : post.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }for post in posts]
            
            return JsonResponse({ "count" : count, "RESULT" : result}, status = 200)

        except KeyError:
            JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)
        except ValueError:
            JsonResponse({'MESSAGE' : 'VALUE_ERROR'}, status = 400)