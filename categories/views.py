from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import Category

def category_to_dict(category):
    return {
        'id': category.id,
        'farsi': category.farsi,
        'english': category.english
    }


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(View):
    
    def get(self, request):
        
        categories = Category.objects.all()
        category_list = [category_to_dict(category) for category in categories]
        return JsonResponse(category_list, safe=False, status=200)
    
    def post(self, request):
        
        try:
            data = json.loads(request.body)
            
            if not data.get('farsi') or not data.get('english'):
                return JsonResponse(
                    {'error': 'فیلدهای farsi و english الزامی هستند'}, 
                    status=400
                )
            
         
            new_category = Category.objects.create(
                farsi=data['farsi'],
                english=data['english']
            )
            
            return JsonResponse(category_to_dict(new_category), status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'داده JSON نامعتبر است'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(View):
    
    def get_category_object(self, category_id):
        """تابع کمکی برای دریافت آبجکت دسته‌بندی"""
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return None
    
    def get(self, request, category_id):
        """GET: دریافت یک دسته‌بندی خاص"""
        category = self.get_category_object(category_id)
        
        if not category:
            return JsonResponse({'error': 'دسته‌بندی یافت نشد'}, status=404)
        
        return JsonResponse(category_to_dict(category), status=200)
    
    def put(self, request, category_id):
        """PUT: آپدیت دسته‌بندی"""
        category = self.get_category_object(category_id)
        
        if not category:
            return JsonResponse({'error': 'دسته‌بندی یافت نشد'}, status=404)
        
        try:
            data = json.loads(request.body)
            
              
            if 'farsi' in data:
                category.farsi = data['farsi']
            
            if 'english' in data:
                category.english = data['english']
            
            category.save()
            return JsonResponse(category_to_dict(category), status=200)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'داده JSON نامعتبر است'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    def delete(self, request, category_id):
        """DELETE: حذف دسته‌بندی"""
        category = self.get_category_object(category_id)
        
        if not category:
            return JsonResponse({'error': 'دسته‌بندی یافت نشد'}, status=404)
        
        category.delete()
        return JsonResponse(
            {'message': 'دسته‌بندی با موفقیت حذف شد'}, 
            status=204
        )