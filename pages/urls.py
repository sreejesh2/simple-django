from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cloudinary/', views.cloudinary_guide, name='cloudinary'),
    path('supabase/', views.supabase_guide, name='supabase'),
    path('render/', views.render_guide, name='render'),
]
