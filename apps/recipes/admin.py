from django.contrib import admin
from .models import Recipe, RecipeIngredient, RecipeStep


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 3
    autocomplete_fields = ('ingredient',)
    fields = ('ingredient', 'quantity', 'is_required')


class RecipeStepInline(admin.StackedInline):
    model = RecipeStep
    extra = 1
    fields = ('step_number', 'instruction', 'image')
    ordering = ('step_number',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'cooking_method', 'difficulty',
        'cooking_time', 'is_spicy', 'popularity', 'is_active',
    )
    list_filter  = ('category', 'cooking_method', 'difficulty', 'is_spicy', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('is_active', 'popularity')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [RecipeIngredientInline, RecipeStepInline]
    fieldsets = (
        ('ข้อมูลทั่วไป', {
            'fields': ('name', 'description', 'image', 'is_active'),
        }),
        ('รายละเอียด', {
            'fields': (
                'category', 'cooking_method', 'difficulty',
                'cooking_time', 'is_spicy', 'calories', 'popularity',
            ),
        }),
        ('ระบบ', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display  = ('recipe', 'ingredient', 'quantity', 'is_required')
    list_filter   = ('is_required',)
    search_fields = ('recipe__name', 'ingredient__name')
    autocomplete_fields = ('ingredient',)


@admin.register(RecipeStep)
class RecipeStepAdmin(admin.ModelAdmin):
    list_display  = ('recipe', 'step_number', 'instruction')
    list_filter   = ('recipe',)
    search_fields = ('recipe__name', 'instruction')
    ordering      = ('recipe', 'step_number')
