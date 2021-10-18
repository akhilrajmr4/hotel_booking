from django.shortcuts import render
import random

# this page admin logined
from app_test.models import *


def adminHome(request):
    return render(request, 'adminHome.html')


# add hotel



def addHotel(request):
    if request.method == "POST":
        hotel_name = request.POST.get('hotel_name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        address = request.POST.get('address', None)
        image_name = "icon-hotel.png"
        password = random.SystemRandom().randint(100000, 999999)
        hotel_details.objects.create(Hotel_name=hotel_name, Email=email, Phone_number=phone, Password=password,
                                     Address =address, Image=image_name)
        
        msg = "Hotel added successfully"
        return render(request, 'addhotel.html', {'msg': msg})
    else:
        return render(request, 'addhotel.html')


# view hotel

def viewHotel(request):
    return render(request, 'viewhotel.html')
