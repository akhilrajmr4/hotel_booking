from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
                  path('adminHome/', views.adminHome, name="adminHome"),  # adminHome page (Akhilraj m r)
                  path('addhotel/', views.addHotel, name="addHotel"),  # addhotel page (Akhilraj m r)
                  path('viewHotel/', views.viewHotel, name="viewHotel"),  # view hotel page (Akhilraj m r)
                  path('viewhotels/delete_hotel/', views.delete_hotel, name="delete_hotel"),  # delete hotel (akhil
                  # raj mr )
                  path('viewhotels/updatehotel/<int:pk>/', views.updatehotel, name="updatehotel"),  # update hotel (akhil raj mr)
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
