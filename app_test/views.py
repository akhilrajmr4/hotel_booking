import json
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
import random
from app_test.models import *


# hotel login

def login(request):
    if request.method == "POST":
        email = request.POST.get('username', None)
        password = request.POST.get('password', None)

        email_ext = hotel_details.objects.filter(Email=email, Password=password)
        if email_ext:
            get_id = hotel_details.objects.get(Email=email, Password=password)
            request.session['id'] = get_id.id
            return render(request, 'hotelhome.html')
        else:
            msg = "Email not exits"
            return render(request, 'login.html', {'msg': msg})
    return render(request, 'login.html')


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

            subject = 'Your site registered by akhilmr'
            message = 'Your login details are below\n\nEmail id : ' + str(email) + '\n\nPassword : ' + str(password) + \
                      '\n\nYou can login this details'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail(subject, message, email_from, recipient_list)

            hotel_details.objects.create(Hotel_name=hotel_name, Email=email, Phone_number=phone,
                                         Password=password, Address=address, Image=image_name)

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


# hotel home

def hotelhome(request):
    if 'id' in request.session:
        return render(request, 'hotelhome.html')
    else:
        return redirect('/')


# hotel delete session
def hotel_delete_session(request):
    del request.session['id']
    request.session.set_expiry(0.0000001)
    return redirect('/')


# update hotel details
def update_hotel(request):
    if 'id' in request.session:
        return render(request, 'updatehoteldetails.html')
    else:
        return redirect('/')


# hotel self details
def hotel_self_details(request):
    if 'id' in request.session:
        hotel_id = request.session['id']
        hotal_datas = hotel_details.objects.get(id=hotel_id)
        return render(request, 'hotelselfdetails.html', {'datas': hotal_datas})
    else:
        return redirect('/')
