from django.urls import path, re_path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    re_path(r'^.*\.html', views.gentella_html, name='gentella'),

    # The home page
    path('', views.index, name='index'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
