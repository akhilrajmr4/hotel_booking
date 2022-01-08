from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.indexpage, name='indexpage'),  # index page (Akhil raj m r)
    # login page (Akhil raj m r)
    path('login_page/', views.login_page, name='login_page'),
    # adminHome page (Akhilraj m r)
    path('admin_logout/', views.admin_logout, name="admin_logout"),
    # admin logout
    path('adminHome/', views.adminHome, name="adminHome"),
    # addhotel page (Akhilraj m r)
    path('addhotel/', views.addHotel, name="addHotel"),
    path('adminHome/delete_hotel/', views.delete_hotel, name="delete_hotel"),
    # delete hotel (akhil raj mr )
    path('adminHome/updatehotel/<int:pk>/', views.updatehotel, name="updatehotel"),
    # delete hotel session (akhil raj m r)
    path('hotel_delete_session/', views.hotel_delete_session, name="hotel_delete_session"),
    # hotelHome (Akhil Raj M R)
    path('hotelhome/', views.hotelhome, name="hotelhome"),
    path('hotel_self_details/', views.hotel_self_details, name="hotel_self_details"),
    # delete hotel session (akhil raj m r)
    path('update_hotel/<int:pk>/', views.update_hotel, name="update_hotel"),
    # update hotel (akhil raj m r)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
