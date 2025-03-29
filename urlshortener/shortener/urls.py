from django.urls import path
from django.http import JsonResponse
from .views import create_short_url, retrieve_original_url, update_short_url, delete_short_url, get_url_statistics

def api_root(request):
    return JsonResponse({"message": "Welcome to the URL shortener API!"})

urlpatterns = [
    path('', api_root, name='api_root'),  # Handles /api/
    path('shorten/', create_short_url, name='create_short_url'),
    path('<str:short_code>/', retrieve_original_url, name='retrieve_url'),
    path('<str:short_code>/update/', update_short_url, name='update_url'),
    path('<str:short_code>/delete/', delete_short_url, name='delete_url'),
    path('<str:short_code>/stats/', get_url_statistics, name='url_stats'),
]
