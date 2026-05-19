"""
Application Layer — Ingredient Use Cases
Business logic เกี่ยวกับวัตถุดิบ
"""
from django.db.models import QuerySet

from .repositories import IngredientRepository


class IngredientService:
    """Use cases สำหรับวัตถุดิบ"""

    def __init__(self, repository: IngredientRepository | None = None) -> None:
        self.repository = repository or IngredientRepository()

    def get_all_grouped(self) -> dict[str, list]:
        """
        คืนวัตถุดิบทั้งหมดจัดกลุ่มตามหมวดหมู่
        ใช้ในหน้า Home สำหรับแสดง ingredient chips
        """
        return self.repository.get_grouped_by_category()

    def get_all(self) -> QuerySet:
        """คืนวัตถุดิบทั้งหมดแบบ flat list"""
        return self.repository.get_all_active()

    def search(self, query: str) -> QuerySet:
        """ค้นหาวัตถุดิบ — ใช้สำหรับ AJAX autocomplete"""
        return self.repository.search(query)

    def get_by_ids(self, ids: list[int]) -> QuerySet:
        """ดึงวัตถุดิบตาม id list — ใช้ในหน้า results"""
        return self.repository.get_by_ids(ids)
