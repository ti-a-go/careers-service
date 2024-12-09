from django.contrib import admin
from django.urls import path

from app.views import ListCreateCareerView, UpdateDeleteCareerView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("careers/", ListCreateCareerView.as_view(), name="careers"),
    path("careers/<str:pk>/", UpdateDeleteCareerView.as_view(), name="careers"),
]
