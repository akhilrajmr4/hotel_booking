import json

from django.http import HttpResponse
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
        image_name = "/static/images/icon-hotel.png"

        hotel_ext = hotel_details.objects.filter(Hotel_name=hotel_name).exists()
        hotel_ext1 = hotel_details.objects.filter(Email=email).exists()

        if hotel_ext or hotel_ext1:
            exit = "Hotel already exist"
            return render(request, 'addhotel.html', {'exit': exit})
        else:
            password = random.SystemRandom().randint(100000, 999999)
            hotel_details.objects.create(Hotel_name=hotel_name, Email=email, Phone_number=phone, Password=password,
                                         Address=address, Image=image_name)

            msg = "Hotel added successfully"
            return render(request, 'addhotel.html', {'msg': msg})
    else:
        return render(request, 'addhotel.html')


# view hotel

def viewHotel(request):
    hotel_det = hotel_details.objects.all().order_by('-id')
    return render(request, 'viewhotel.html', {'hotel_det': hotel_det})


# delete hotel

def delete_hotel(request):
    delete_id = request.GET.get('id')
    del_data = hotel_details.objects.get(id=delete_id)
    del_data.delete()
    msg = "Hotel deleted"
    return HttpResponse(json.dumps({'msg': msg}))


# update hotel

def updatehotel(request, pk):
    if request.method == "POST":

        hotel_data = hotel_details.objects.get(id=pk)

        hotel_name = request.POST.get('hotel_name', None)
        email = request.POST.get('email', None)

        hotel_ext = hotel_details.objects.filter(Hotel_name=hotel_name).exists()
        hotel_ext1 = hotel_details.objects.filter(Email=email).exists()

        if hotel_ext or hotel_ext1:
            exits = "Already exist"
            return render(request, 'updatehotel.html', {'exits': exits})
        else:
            hotel_data.Hotel_name = hotel_name
            hotel_data.Email = email
            hotel_data.Phone_number = request.POST.get('phone', None)
            hotel_data.Address = request.POST.get('address', None)
            hotel_data.save()
            msg = "Hotel update successfully"
            return render(request, 'updatehotel.html', {'msg': msg})

    else:
        hotel_data = hotel_details.objects.get(id=pk)
        return render(request, 'updatehotel.html', {'hotel_data': hotel_data})
