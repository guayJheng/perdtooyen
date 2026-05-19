from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Recommendations: home (/) and /recommend/
    path('', include('recommendations.urls')),
    # Recipes: /recipes/ and /recipes/<id>/
    path('recipes/', include('recipes.urls')),
    # Ingredients API: /api/ingredients/
    path('api/', include('ingredients.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
