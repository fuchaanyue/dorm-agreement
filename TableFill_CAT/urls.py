# urls.py
from django.contrib import admin
from django.urls import path
from records import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('api/save_image/', views.save_image, name="save_image"),
]
