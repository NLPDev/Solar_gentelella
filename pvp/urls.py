from django.contrib import admin
from django.urls import path
from .views import home, PVPowerData, results
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home, name='home'),
    path('results/pvpchart/data/', PVPowerData.as_view()),
    path('results', results, name='results'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
