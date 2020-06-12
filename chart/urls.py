from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView, ChartData


urlpatterns = [
    path('', HomeView.as_view(), name='charts'),
    path('api/', ChartData.as_view()),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
