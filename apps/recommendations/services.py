"""
Application Layer — Recommendation Use Case
Core business logic: คำนวณ match % และเรียงลำดับเมนูที่แนะนำ
"""
from dataclasses import dataclass, field

from recipes.repositories import RecipeRepository
from ingredients.repositories import IngredientRepository


@dataclass
class RecipeMatch:
    """
    Value Object ที่เก็บผลลัพธ์การจับคู่เมนูกับวัตถุดิบที่ผู้ใช้มี
    """
    recipe: object                         # Recipe instance
    match_percentage: float                # % วัตถุดิบที่ตรง
    matched_count: int                     # จำนวนวัตถุดิบที่ตรง
    total_required: int                    # จำนวนวัตถุดิบหลักทั้งหมด
    missing_ingredients: list = field(default_factory=list)  # Ingredient instances ที่ขาด

    @property
    def match_class(self) -> str:
        """CSS class สำหรับ match bar"""
        if self.match_percentage >= 80:
            return 'high'
        elif self.match_percentage >= 50:
            return 'medium'
        return 'low'

    @property
    def match_label(self) -> str:
        if self.match_percentage == 100:
            return 'ทำได้เลย!'
        elif self.match_percentage >= 80:
            return 'เกือบครบ'
        elif self.match_percentage >= 50:
            return 'มีบางส่วน'
        return 'ขาดหลายอย่าง'


class RecommendationService:
    """
    Use Case: แนะนำเมนูจากวัตถุดิบที่ผู้ใช้มี

    Algorithm:
        1. ดึงเมนู active ทั้งหมด
        2. สำหรับแต่ละเมนู: คำนวณ match_pct จากวัตถุดิบหลัก (is_required=True)
        3. เรียงลำดับ:  match_pct DESC → difficulty (easy first) → popularity DESC
        4. คืน list[RecipeMatch] (กรองเมนูที่ match 0% ออก)
    """

    DIFFICULTY_ORDER = {'easy': 0, 'medium': 1, 'hard': 2}

    def __init__(
        self,
        recipe_repo: RecipeRepository | None = None,
        ingredient_repo: IngredientRepository | None = None,
    ) -> None:
        self.recipe_repo = recipe_repo or RecipeRepository()
        self.ingredient_repo = ingredient_repo or IngredientRepository()

    def recommend(self, user_ingredient_ids: list[int]) -> list[RecipeMatch]:
        """
        คืน list[RecipeMatch] เรียงตามความเหมาะสม
        """
        user_ids: set[int] = set(int(i) for i in user_ingredient_ids if i)

        if not user_ids:
            return []

        recipes = self.recipe_repo.get_all_active()
        matches: list[RecipeMatch] = []

        for recipe in recipes:
            required_ris = list(recipe.required_ingredients)
            if not required_ris:
                continue

            required_ids = {ri.ingredient_id for ri in required_ris}
            matched_ids = required_ids & user_ids
            missing_ids = required_ids - user_ids

            match_pct = len(matched_ids) / len(required_ids) * 100

            # กรองเมนูที่ไม่ตรงเลย
            if match_pct == 0:
                continue

            missing_ingredients = [
                ri.ingredient for ri in required_ris
                if ri.ingredient_id in missing_ids
            ]

            matches.append(RecipeMatch(
                recipe=recipe,
                match_percentage=round(match_pct, 1),
                matched_count=len(matched_ids),
                total_required=len(required_ids),
                missing_ingredients=missing_ingredients,
            ))

        # เรียงลำดับ
        matches.sort(key=lambda m: (
            -m.match_percentage,
            self.DIFFICULTY_ORDER.get(m.recipe.difficulty, 1),
            -m.recipe.popularity,
        ))

        return matches
