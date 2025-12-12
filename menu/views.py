from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import MenuItem
from categories.models import Category

def menuitem_to_dict(menuitem):
    return {
        'id': menuitem.id,
        'name': menuitem.name,
        'description': menuitem.description if menuitem.description else "",
        'price': str(menuitem.price),  
        'category': {
            'id': menuitem.category.id,
            'farsi': menuitem.category.farsi,
            'english': menuitem.category.english
        }
    }

@method_decorator(csrf_exempt, name='dispatch')
class MenuItemListView(View):
    
    def get(self, request):
        category_id = request.GET.get('category_id')
        
        if category_id:
            menu_items = MenuItem.objects.filter(category_id=category_id)
        else:
            menu_items = MenuItem.objects.all()
        
        menu_item_list = [menuitem_to_dict(item) for item in menu_items]
        return JsonResponse(menu_item_list, safe=False, status=200)
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if not data.get('name'):
                return JsonResponse({'error': 'فیلد name الزامی است'}, status=400)
            
            if not data.get('price'):
                return JsonResponse({'error': 'فیلد price الزامی است'}, status=400)
            
            if not data.get('category_id'):
                return JsonResponse({'error': 'فیلد category_id الزامی است'}, status=400)
            
            try:
                category = Category.objects.get(id=data['category_id'])
            except Category.DoesNotExist:
                return JsonResponse({'error': 'دسته‌بندی یافت نشد'}, status=400)
            
            new_item = MenuItem.objects.create(
                name=data['name'],
                description=data.get('description', ''), 
                price=data['price'],
                category=category
            )
            
            return JsonResponse(menuitem_to_dict(new_item), status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'داده JSON نامعتبر است'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class MenuItemDetailView(View):
    
    def get_menuitem_object(self, menuitem_id):
        try:
            return MenuItem.objects.get(id=menuitem_id)
        except MenuItem.DoesNotExist:
            return None
    
    def get(self, request, menuitem_id):
        menu_item = self.get_menuitem_object(menuitem_id)
        
        if not menu_item:
            return JsonResponse({'error': 'آیتم منو یافت نشد'}, status=404)
        
        return JsonResponse(menuitem_to_dict(menu_item), status=200)
    
    def put(self, request, menuitem_id):
        menu_item = self.get_menuitem_object(menuitem_id)
        
        if not menu_item:
            return JsonResponse({'error': 'آیتم منو یافت نشد'}, status=404)
        
        try:
            data = json.loads(request.body)
            
            if 'name' in data:
                menu_item.name = data['name']
            
            if 'description' in data:
                menu_item.description = data['description']
            
            if 'price' in data:
                menu_item.price = data['price']
            
            if 'category_id' in data:
                try:
                    category = Category.objects.get(id=data['category_id'])
                    menu_item.category = category
                except Category.DoesNotExist:
                    return JsonResponse({'error': 'دسته‌بندی یافت نشد'}, status=400)
            
            menu_item.save()
            return JsonResponse(menuitem_to_dict(menu_item), status=200)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'داده JSON نامعتبر است'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    def delete(self, request, menuitem_id):
        menu_item = self.get_menuitem_object(menuitem_id)
        
        if not menu_item:
            return JsonResponse({'error': 'آیتم منو یافت نشد'}, status=404)
        
        menu_item.delete()
        return JsonResponse(
            {'message': 'آیتم منو با موفقیت حذف شد'}, 
            status=204
        )
        