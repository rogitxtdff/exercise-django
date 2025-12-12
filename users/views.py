from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import User

def user_to_dict(user):
    return {
        'id': user.id,
        'name': user.name,
        'username': user.username,
        'password': user.password
    }

@method_decorator(csrf_exempt, name='dispatch')
class UserListView(View):
    
    def get(self, request):
        users = User.objects.all()
        user_list = [user_to_dict(user) for user in users]
        return JsonResponse(user_list, safe=False, status=200)
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if User.objects.filter(username=data['username']).exists():
                return JsonResponse(
                    {'error': 'این نام کاربری از قبل موجود است'}, 
                    status=400
                )
            
            new_user = User.objects.create(
                name=data['name'],
                username=data['username'],
                password=data['password']
            )
            
            return JsonResponse(user_to_dict(new_user), status=201)
            
        except KeyError as e:
            return JsonResponse(
                {'error': f'فیلد {str(e)} الزامی است'}, 
                status=400
            )
        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'داده JSON نامعتبر است'}, 
                status=400
            )
        except Exception as e:
            return JsonResponse(
                {'error': str(e)}, 
                status=400
            )

@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(View):
    
    def get_user_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    def get(self, request, user_id):
        user = self.get_user_object(user_id)
        
        if not user:
            return JsonResponse(
                {'error': 'کاربر یافت نشد'}, 
                status=404
            )
        
        return JsonResponse(user_to_dict(user), status=200)
    
    def put(self, request, user_id):
        user = self.get_user_object(user_id)
        
        if not user:
            return JsonResponse(
                {'error': 'کاربر یافت نشد'}, 
                status=404
            )
        
        try:
            data = json.loads(request.body)
            
            if 'name' in data:
                user.name = data['name']
            
            if 'username' in data:
                new_username = data['username']
                if new_username != user.username:
                    if User.objects.filter(username=new_username).exists():
                        return JsonResponse(
                            {'error': 'این نام کاربری از قبل موجود است'}, 
                            status=400
                        )
                    user.username = new_username
            
            if 'password' in data:
                user.password = data['password']
            
            user.save()
            return JsonResponse(user_to_dict(user), status=200)
            
        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'داده JSON نامعتبر است'}, 
                status=400
            )
        except Exception as e:
            return JsonResponse(
                {'error': str(e)}, 
                status=400
            )
    
    def delete(self, request, user_id):
        user = self.get_user_object(user_id)
        
        if not user:
            return JsonResponse(
                {'error': 'کاربر یافت نشد'}, 
                status=404
            )
        
        user.delete()
        return JsonResponse(
            {'message': 'کاربر با موفقیت حذف شد'}, 
            status=204
        )