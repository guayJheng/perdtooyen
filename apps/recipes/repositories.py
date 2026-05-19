"""
Infrastructure Layer — Recipe Repository
ทำหน้าที่เป็น gateway ระหว่าง application layer กับ Django ORM
"""
from django.db.models import QuerySet, Q

from .models import Recipe


class RecipeRepository:
    """Data-access object for Recipe."""

    def _base_qs(self) -> QuerySet:
        return (
            Recipe.objects
            .filter(is_active=True)
            .prefetch_related(
                'recipe_ingredients__ingredient',
                'steps',
            )
        )

    def get_all_active(self) -> QuerySet:
        """คืนเมนูทั้งหมดที่ active พร้อม prefetch"""
        return self._base_qs().order_by('-popularity', 'name')

    def get_by_id(self, recipe_id: int) -> Recipe:
        """คืนเมนูตาม pk (raise DoesNotExist ถ้าไม่พบ)"""
        return self._base_qs().get(id=recipe_id)

    def search(self, query: str) -> QuerySet:
        """ค้นหาเมนูตามชื่อ, คำอธิบาย หรือวัตถุดิบ"""
        if not query:
            return self.get_all_active()
        return (
            self._base_qs()
            .filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(recipe_ingredients__ingredient__name__icontains=query)
            )
            .distinct()
            .order_by('-popularity', 'name')
        )

    def filter_by(
        self,
        category: str | None = None,
        cooking_method: str | None = None,
        difficulty: str | None = None,
        max_time: int | None = None,
        is_spicy: bool | None = None,
    ) -> QuerySet:
        """กรองเมนูตามเงื่อนไขต่าง ๆ"""
        qs = self._base_qs()
        if category:
            qs = qs.filter(category=category)
        if cooking_method:
            qs = qs.filter(cooking_method=cooking_method)
        if difficulty:
            qs = qs.filter(difficulty=difficulty)
        if max_time is not None:
            qs = qs.filter(cooking_time__lte=max_time)
        if is_spicy is not None:
            qs = qs.filter(is_spicy=is_spicy)
        return qs.order_by('-popularity', 'name')
