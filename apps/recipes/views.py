"""
Interface Layer — Recipes Views
"""
from django.shortcuts import render, get_object_or_404

from .services import RecipeService
from .models import Recipe

_service = RecipeService()

# Choices สำหรับ filter dropdowns ในหน้า list
CATEGORY_CHOICES = Recipe.CATEGORY_CHOICES
COOKING_METHOD_CHOICES = Recipe.COOKING_METHOD_CHOICES
DIFFICULTY_CHOICES = Recipe.DIFFICULTY_CHOICES


def recipe_list(request):
    """
    GET /recipes/
    แสดงเมนูทั้งหมดพร้อม filter และ search bar
    """
    category       = request.GET.get('category', '').strip()
    cooking_method = request.GET.get('cooking_method', '').strip()
    difficulty     = request.GET.get('difficulty', '').strip()
    is_spicy_raw   = request.GET.get('is_spicy', '').strip()
    max_time_raw   = request.GET.get('max_time', '').strip()
    query          = request.GET.get('q', '').strip()

    # ถ้ามี search query ให้ค้นหาก่อน แล้วค่อย filter
    if query:
        recipes = _service.search(query)
    else:
        is_spicy = None
        if is_spicy_raw == '1':
            is_spicy = True

        max_time = int(max_time_raw) if max_time_raw.isdigit() else None

        recipes = _service.get_filtered(
            category=category or None,
            cooking_method=cooking_method or None,
            difficulty=difficulty or None,
            max_time=max_time,
            is_spicy=is_spicy,
        )

    context = {
        'recipes':               recipes,
        'query':                 query,
        'selected_category':     category,
        'selected_method':       cooking_method,
        'selected_difficulty':   difficulty,
        'selected_is_spicy':     is_spicy_raw,
        'selected_max_time':     max_time_raw,
        'category_choices':      CATEGORY_CHOICES,
        'method_choices':        COOKING_METHOD_CHOICES,
        'difficulty_choices':    DIFFICULTY_CHOICES,
        'total':                 recipes.count() if hasattr(recipes, 'count') else len(recipes),
    }
    return render(request, 'recipes/list.html', context)


def recipe_detail(request, pk: int):
    """
    GET /recipes/<pk>/
    แสดงรายละเอียดเมนู พร้อมแสดงวัตถุดิบที่ขาดจาก session
    """
    recipe = get_object_or_404(Recipe, pk=pk, is_active=True)

    # ดึง ingredient IDs ที่ผู้ใช้เลือกไว้จาก session
    user_ingredient_ids: set[int] = set(
        request.session.get('selected_ingredient_ids', [])
    )

    # คำนวณวัตถุดิบที่มี / ขาด สำหรับแต่ละ ingredient ในเมนูนี้
    ingredient_status = []
    for ri in recipe.all_ingredients:
        ingredient_status.append({
            'recipe_ingredient': ri,
            'has_it': ri.ingredient_id in user_ingredient_ids,
        })

    steps = recipe.steps.order_by('step_number')

    context = {
        'recipe':             recipe,
        'ingredient_status':  ingredient_status,
        'steps':              steps,
        'has_session':        bool(user_ingredient_ids),
    }
    return render(request, 'recipes/detail.html', context)


def search(request):
    """
    GET /recipes/search/?q=<query>
    ค้นหาเมนูตามชื่อ, คำอธิบาย หรือวัตถุดิบ
    """
    query = request.GET.get('q', '').strip()
    recipes = _service.search(query) if query else []

    context = {
        'recipes': recipes,
        'query':   query,
        'total':   recipes.count() if hasattr(recipes, 'count') else len(recipes),
    }
    return render(request, 'recipes/search.html', context)
