from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import User

# تابع کمکی برای تبدیل آبجکت User به دیکشنری
def user_to_dict(user):
    return {
        'id': user.id,
        'name': user.name,
        'username': user.username,
        'password': user.password
    }

# کلاس برای مدیریت لیست کاربران (GET همه, POST جدید)
@method_decorator(csrf_exempt, name='dispatch')
class UserListView(View):
    
    def get(self, request):
        """GET: دریافت لیست همه کاربران"""
        users = User.objects.all()
        user_list = [user_to_dict(user) for user in users]
        return JsonResponse(user_list, safe=False, status=200)
    
    def post(self, request):
        """POST: ساخت کاربر جدید"""
        try:
            data = json.loads(request.body)
            
            # بررسی وجود username تکراری
            if User.objects.filter(username=data['username']).exists():
                return JsonResponse(
                    {'error': 'این نام کاربری از قبل موجود است'}, 
                    status=400
                )
            
            # ساخت کاربر جدید
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

# کلاس برای مدیریت یک کاربر خاص (GET, PUT, DELETE)
@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(View):
    
    def get_user_object(self, user_id):
        """تابع کمکی برای دریافت آبجکت کاربر"""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    def get(self, request, user_id):
        """GET: دریافت یک کاربر خاص"""
        user = self.get_user_object(user_id)
        
        if not user:
            return JsonResponse(
                {'error': 'کاربر یافت نشد'}, 
                status=404
            )
        
        return JsonResponse(user_to_dict(user), status=200)
    
    def put(self, request, user_id):
        """PUT: آپدیت کاربر"""
        user = self.get_user_object(user_id)
        
        if not user:
            return JsonResponse(
                {'error': 'کاربر یافت نشد'}, 
                status=404
            )
        
        try:
            data = json.loads(request.body)
            
            # آپدیت فیلدها
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
        """DELETE: حذف کاربر"""
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