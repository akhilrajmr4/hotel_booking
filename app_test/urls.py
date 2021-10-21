from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
                  path('', views.login, name='login'),  # login page (Akhil raj m r)
                  path('adminHome/', views.adminHome, name="adminHome"),  # adminHome page (Akhilraj m r)
                  path('addhotel/', views.addHotel, name="addHotel"),  # addhotel page (Akhilraj m r)
                  path('viewHotel/', views.viewHotel, name="viewHotel"),  # view hotel page (Akhilraj m r)
                  path('viewhotels/delete_hotel/', views.delete_hotel, name="delete_hotel"),  # delete hotel (akhil
                  # raj mr )
                  path('viewhotels/updatehotel/<int:pk>/', views.updatehotel, name="updatehotel"),
                  # update hotel (akhil raj mr)
                  path('hotel_delete_session/', views.hotel_delete_session, name="hotel_delete_session"),
                  # delete hotel session (akhil raj m r)
                  path('hotel_self_details/', views.hotel_self_details, name="hotel_self_details"),
                  # delete hotel session (akhil raj m r)
                  path('update_hotel/<int:pk>/', views.update_hotel, name="update_hotel"),
                  # update hotel (akhil raj m r)

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
