# foods/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('generate-similar-foods/', views.generate_similar_foods, name='generate-similar-foods'),
    path('meals/', views.meal_list, name='meal-list'),
    path('extract-and-save-meal-info/', views.extract_and_save_meal_info, name='extract-and-save-meal-info'),
    path('upload-image/', views.upload_image, name='upload-image'),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
