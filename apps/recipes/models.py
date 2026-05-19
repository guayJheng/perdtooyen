from django.db import models
from ingredients.models import Ingredient


class Recipe(models.Model):
    """
    Domain Entity: เมนูอาหาร
    """
    DIFFICULTY_CHOICES = [
        ('easy',   'ง่าย'),
        ('medium', 'ปานกลาง'),
        ('hard',   'ยาก'),
    ]
    CATEGORY_CHOICES = [
        ('thai',          'อาหารไทย'),
        ('street',        'อาหารตามสั่ง'),
        ('international', 'อาหารนานาชาติ'),
    ]
    COOKING_METHOD_CHOICES = [
        ('fried',   'เมนูทอด'),
        ('boiled',  'เมนูต้ม'),
        ('stirfry', 'เมนูผัด'),
        ('salad',   'เมนูยำ / สลัด'),
        ('grill',   'เมนูย่าง'),
        ('soup',    'เมนูแกง / ซุป'),
        ('other',   'อื่น ๆ'),
    ]

    name = models.CharField(max_length=200, verbose_name='ชื่อเมนู')
    description = models.TextField(blank=True, verbose_name='คำอธิบาย')
    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        null=True,
        verbose_name='รูปภาพ',
    )
    cooking_time = models.PositiveIntegerField(verbose_name='เวลาทำ (นาที)')
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='easy',
        verbose_name='ระดับความยาก',
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='thai',
        verbose_name='หมวดหมู่',
    )
    cooking_method = models.CharField(
        max_length=10,
        choices=COOKING_METHOD_CHOICES,
        default='other',
        verbose_name='วิธีทำ',
    )
    is_spicy = models.BooleanField(default=False, verbose_name='เผ็ด')
    calories = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='แคลอรี่ (kcal)',
    )
    popularity = models.PositiveIntegerField(default=0, verbose_name='ความนิยม')
    is_active = models.BooleanField(default=True, verbose_name='เผยแพร่')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'เมนูอาหาร'
        verbose_name_plural = 'เมนูอาหารทั้งหมด'
        ordering = ['-popularity', 'name']

    def __str__(self) -> str:
        return self.name

    def get_difficulty_badge_class(self) -> str:
        return {
            'easy':   'badge-success',
            'medium': 'badge-warning',
            'hard':   'badge-danger',
        }.get(self.difficulty, 'badge-secondary')

    def get_cooking_method_emoji(self) -> str:
        return {
            'fried':   '🍳',
            'boiled':  '🍲',
            'stirfry': '🥢',
            'salad':   '🥗',
            'grill':   '🔥',
            'soup':    '🍛',
            'other':   '🍽️',
        }.get(self.cooking_method, '🍽️')

    @property
    def required_ingredients(self):
        """Return queryset of required RecipeIngredient rows."""
        return self.recipe_ingredients.filter(is_required=True).select_related('ingredient')

    @property
    def all_ingredients(self):
        """Return queryset of all RecipeIngredient rows."""
        return self.recipe_ingredients.all().select_related('ingredient')


class RecipeIngredient(models.Model):
    """
    Domain Entity: วัตถุดิบในเมนู (ตาราง junction)
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='เมนู',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='วัตถุดิบ',
    )
    quantity = models.CharField(
        max_length=80,
        blank=True,
        verbose_name='ปริมาณ',
        help_text='เช่น 2 ช้อนโต๊ะ, 1 ฟอง, 200g',
    )
    is_required = models.BooleanField(
        default=True,
        verbose_name='วัตถุดิบหลัก',
        help_text='หากไม่เลือก จะถือว่าเป็นวัตถุดิบเสริม (optional)',
    )

    class Meta:
        verbose_name = 'วัตถุดิบในเมนู'
        verbose_name_plural = 'วัตถุดิบในเมนูทั้งหมด'
        unique_together = ('recipe', 'ingredient')

    def __str__(self) -> str:
        return f'{self.recipe.name} — {self.ingredient.name}'


class RecipeStep(models.Model):
    """
    Domain Entity: ขั้นตอนการทำอาหาร
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='steps',
        verbose_name='เมนู',
    )
    step_number = models.PositiveIntegerField(verbose_name='ขั้นตอนที่')
    instruction = models.TextField(verbose_name='คำอธิบายขั้นตอน')
    image = models.ImageField(
        upload_to='steps/',
        blank=True,
        null=True,
        verbose_name='รูปภาพขั้นตอน',
    )

    class Meta:
        verbose_name = 'ขั้นตอนการทำ'
        verbose_name_plural = 'ขั้นตอนการทำทั้งหมด'
        ordering = ['recipe', 'step_number']
        unique_together = ('recipe', 'step_number')

    def __str__(self) -> str:
        return f'{self.recipe.name} — ขั้นตอน {self.step_number}'
