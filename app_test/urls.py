from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('adminHome/', views.adminHome, name="adminHome"), # adminHome page (Akhilraj m r)
    path('addhotel/', views.addHotel, name="addHotel"), # adminHome page (Akhilraj m r)
    path('viewHotel/', views.viewHotel, name="viewHotel"), # adminHome page (Akhilraj m r)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)