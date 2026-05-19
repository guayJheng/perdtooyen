"""
Infrastructure Layer — Ingredient Repository
ทำหน้าที่เป็น gateway ระหว่าง application layer กับ Django ORM
Views และ Services ไม่ควรเรียก Ingredient.objects โดยตรง
"""
from django.db.models import QuerySet

from .models import Ingredient


class IngredientRepository:
    """Data-access object for Ingredient."""

    def get_all_active(self) -> QuerySet:
        """คืนวัตถุดิบทั้งหมดที่ active เรียงตามหมวดหมู่และชื่อ"""
        return Ingredient.objects.filter(is_active=True).order_by('category', 'name')

    def get_by_ids(self, ids: list[int]) -> QuerySet:
        """คืนวัตถุดิบตาม primary key list"""
        return Ingredient.objects.filter(id__in=ids, is_active=True)

    def search(self, query: str) -> QuerySet:
        """ค้นหาวัตถุดิบตามชื่อ (case-insensitive)"""
        if not query:
            return self.get_all_active()
        return Ingredient.objects.filter(
            name__icontains=query,
            is_active=True,
        ).order_by('category', 'name')

    def get_grouped_by_category(self) -> dict[str, list]:
        """คืน dict {category_label: [Ingredient, ...]}"""
        ingredients = self.get_all_active()
        grouped: dict[str, list] = {}
        for ingredient in ingredients:
            label = ingredient.get_category_display()
            if label not in grouped:
                grouped[label] = []
            grouped[label].append(ingredient)
        return grouped
