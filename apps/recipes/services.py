"""
Application Layer — Recipe Use Cases
Business logic เกี่ยวกับเมนูอาหาร
"""
from django.db.models import QuerySet

from .repositories import RecipeRepository
from .models import Recipe


class RecipeService:
    """Use cases สำหรับเมนูอาหาร"""

    def __init__(self, repository: RecipeRepository | None = None) -> None:
        self.repository = repository or RecipeRepository()

    def get_all(self) -> QuerySet:
        """คืนเมนูทั้งหมด"""
        return self.repository.get_all_active()

    def get_detail(self, recipe_id: int) -> Recipe:
        """
        คืนรายละเอียดเมนู
        raise Recipe.DoesNotExist ถ้าไม่พบ
        """
        return self.repository.get_by_id(recipe_id)

    def search(self, query: str) -> QuerySet:
        """ค้นหาเมนูตามชื่อหรือวัตถุดิบ"""
        return self.repository.search(query)

    def get_filtered(
        self,
        category: str | None = None,
        cooking_method: str | None = None,
        difficulty: str | None = None,
        max_time: int | None = None,
        is_spicy: bool | None = None,
    ) -> QuerySet:
        """
        กรองเมนูตามเงื่อนไข
        รองรับ SRS 3.1.5 Filter Feature
        """
        return self.repository.filter_by(
            category=category,
            cooking_method=cooking_method,
            difficulty=difficulty,
            max_time=max_time,
            is_spicy=is_spicy,
        )
