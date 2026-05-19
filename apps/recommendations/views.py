"""
Interface Layer — Recommendations Views
หน้า Home (เลือกวัตถุดิบ) และหน้าผลลัพธ์การแนะนำ
"""
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from ingredients.services import IngredientService
from .services import RecommendationService

_ingredient_service    = IngredientService()
_recommendation_service = RecommendationService()


def home(request):
    """
    GET /
    หน้าหลัก — แสดง ingredient chips จัดกลุ่มตามหมวดหมู่
    """
    grouped_ingredients = _ingredient_service.get_all_grouped()
    all_ingredients     = _ingredient_service.get_all()

    # กู้คืน ingredient IDs ที่เคยเลือกไว้ใน session
    saved_ids = set(request.session.get('selected_ingredient_ids', []))

    context = {
        'grouped_ingredients': grouped_ingredients,
        'all_ingredients':     all_ingredients,
        'saved_ids':           saved_ids,
    }
    return render(request, 'home.html', context)


@require_http_methods(['POST'])
def recommend(request):
    """
    POST /recommend/
    รับ ingredient_ids จาก form แล้วคำนวณและแสดงผลการแนะนำ
    """
    raw_ids = request.POST.getlist('ingredient_ids')
    ingredient_ids = [int(i) for i in raw_ids if i.isdigit()]

    # บันทึกลง session เพื่อใช้ใน recipe detail
    request.session['selected_ingredient_ids'] = ingredient_ids

    # ดึงข้อมูลวัตถุดิบที่เลือก (สำหรับแสดงใน template)
    selected_ingredients = _ingredient_service.get_by_ids(ingredient_ids)

    # คำนวณการแนะนำ
    matches = _recommendation_service.recommend(ingredient_ids)

    context = {
        'matches':              matches,
        'selected_ingredients': selected_ingredients,
        'selected_count':       len(ingredient_ids),
        'result_count':         len(matches),
    }
    return render(request, 'recommendations/results.html', context)
