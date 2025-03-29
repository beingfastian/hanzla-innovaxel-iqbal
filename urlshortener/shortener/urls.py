from django.urls import path
from . import views

urlpatterns = [
    path('shorten', views.create_short_url, name='create_short_url'),
    path('shorten/<str:short_code>', views.retrieve_original_url, name='retrieve_url'),
    path('shorten/<str:short_code>/update', views.update_short_url, name='update_url'),
    path('shorten/<str:short_code>/delete', views.delete_short_url, name='delete_url'),
    path('shorten/<str:short_code>/stats', views.get_url_statistics, name='url_stats'),
]