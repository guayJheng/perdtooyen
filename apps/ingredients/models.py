from django.db import models


class Ingredient(models.Model):
    """
    Domain Entity: วัตถุดิบ
    แต่ละวัตถุดิบมีชื่อและหมวดหมู่
    """
    CATEGORY_CHOICES = [
        ('protein', 'โปรตีน (เนื้อสัตว์ / ไข่ / อาหารทะเล)'),
        ('veggie',  'ผักและเครื่องเคียง'),
        ('spice',   'เครื่องเทศและสมุนไพร'),
        ('grain',   'ข้าวและแป้ง'),
        ('sauce',   'เครื่องปรุงและซอส'),
        ('other',   'อื่น ๆ'),
    ]

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='ชื่อวัตถุดิบ',
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other',
        verbose_name='หมวดหมู่',
    )
    is_active = models.BooleanField(default=True, verbose_name='ใช้งานอยู่')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'วัตถุดิบ'
        verbose_name_plural = 'วัตถุดิบทั้งหมด'
        ordering = ['category', 'name']

    def __str__(self) -> str:
        return self.name

    def get_category_icon(self) -> str:
        icons = {
            'protein': '🥩',
            'veggie':  '🥦',
            'spice':   '🌶️',
            'grain':   '🌾',
            'sauce':   '🧂',
            'other':   '🫙',
        }
        return icons.get(self.category, '🫙')
