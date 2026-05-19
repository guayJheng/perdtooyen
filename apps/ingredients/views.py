"""
Interface Layer — Ingredients Views
AJAX endpoint สำหรับค้นหาวัตถุดิบ
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .services import IngredientService

_service = IngredientService()


@require_GET
def ingredient_search_api(request):
    """
    GET /api/ingredients/?q=<query>
    คืน JSON list ของวัตถุดิบที่ตรงกับ query
    ใช้สำหรับ AJAX search บนหน้า Home
    """
    query = request.GET.get('q', '').strip()
    ingredients = _service.search(query)
    data = [
        {
            'id': ing.id,
            'name': ing.name,
            'category': ing.category,
            'category_label': ing.get_category_display(),
            'icon': ing.get_category_icon(),
        }
        for ing in ingredients[:30]
    ]
    return JsonResponse({'ingredients': data})
