import json
import os
from django.contrib.auth import authenticate, login, logout

from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import random

from django.urls import reverse

from app_test.models import *

# index page


def indexpage(request):
    return render(request, 'index.html')


# hotel login

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        email_ext = hotel_details.objects.filter(Email=username, Password=password)
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('adminHome')
        else:
            if email_ext:
                get_id = hotel_details.objects.get(Email=username, Password=password)
                request.session['id'] = get_id.id
                return redirect('hotelhome')
            else:
                msg = "Email not exits"
                return render(request, 'login.html', {'msg': msg})
    else:
        return render(request, 'login.html')


def admin_logout(request):
    logout(request)
    return redirect('login_page')

def adminHome(request):

    if request.user.is_authenticated:
        return render(request, 'adminHome.html')
    else:
        return redirect('login_page')


# add hotel

def addHotel(request):

    if request.user.is_authenticated:
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

                # subject = 'Your site registered by akhilmr'
                # message = 'Your login details are below\n\nEmail id : ' + str(email) + '\n\nPassword : ' + str(password) + \
                #           '\n\nYou can login this details'
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = [email, ]
                # send_mail(subject, message, email_from, recipient_list)

                hotel_details.objects.create(Hotel_name=hotel_name, Email=email, Phone_number=phone,
                                            Password=password, Address=address, Image=image_name)

                msg = "Hotel added successfully"
                return render(request, 'addhotel.html', {'msg': msg})
        else:
            return render(request, 'addhotel.html')
    else:
        return redirect('login_page')


# view hotel

def viewHotel(request):
    if request.user.is_authenticated:
        hotel_det = hotel_details.objects.all().order_by('?')
        return render(request, 'viewhotel.html', {'hotel_det': hotel_det})
    else:
        return redirect('login_page')


# delete hotel

def delete_hotel(request):

    if request.user.is_authenticated:
        delete_id = request.GET.get('id')
        del_data = hotel_details.objects.get(id=delete_id)
        del_data.delete()
        msg = "Hotel deleted"
        return HttpResponse(json.dumps({'msg': msg}))
    else:
        return redirect('login_page')


# update hotel

def updatehotel(request, pk):

    if request.user.is_authenticated:

        if request.method == "POST":

            hotel_data = hotel_details.objects.get(id=pk)

            hotel_name = request.POST.get('hotel_name', None)
            email = request.POST.get('email', None)

            if hotel_data.Hotel_name == hotel_name and hotel_data.Email == email:
                hotel_data.Hotel_name = hotel_name
                hotel_data.Email = email
                hotel_data.Phone_number = request.POST.get('phone', None)
                hotel_data.Address = request.POST.get('address', None)
                hotel_data.save()
                return redirect('viewHotel')

            elif hotel_details.objects.filter(Hotel_name=hotel_name) and hotel_details.objects.filter(Email=email):
                exits = "Already exist"
                return render(request, 'updatehotel.html', {'exits': exits})
            else:
                hotel_data.Hotel_name = hotel_name
                hotel_data.Email = email
                hotel_data.Phone_number = request.POST.get('phone', None)
                hotel_data.Address = request.POST.get('address', None)
                hotel_data.save()
                return redirect('viewHotel')

        else:
            hotel_data = hotel_details.objects.get(id=pk)
            return render(request, 'updatehotel.html', {'hotel_data': hotel_data})
    
    else:
        return redirect('login_page')


# hotel home

def hotelhome(request):
    if 'id' in request.session:
        return render(request, 'hotelhome.html')
    else:
        return redirect('/')


# hotel delete session
def hotel_delete_session(request):

    if 'id' in request.session:
        # for key in request.session.keys():
        #     del request.session[key]
        request.session.flush()
        # request.session.set_expiry(0.0000001)
        return redirect('login_page')
    else:
        return redirect('login_page')


# update hotel details
def update_hotel(request, pk):
    if 'id' in request.session:
        if request.method == "POST":
            self_hotel = hotel_details.objects.get(id=pk)
            if request.FILES.get('file') is not None:
                if self_hotel.Image != "/static/images/icon-hotel.png":
                    os.remove(self_hotel.Image.path)
                self_hotel.Image = request.FILES['file']

            Hotel_name = request.POST.get('hotel_name', None)
            self_hotel.Email = request.POST.get('email', None)
            self_hotel.Phone_number = request.POST.get('phone', None)
            self_hotel.Address = request.POST.get('address', None)
            self_hotel.Description = request.POST.get('description', None)

            if self_hotel.Hotel_name == Hotel_name:
                self_hotel.Hotel_name = Hotel_name
                self_hotel.save()
                return redirect('hotel_self_details')

            elif hotel_details.objects.filter(Hotel_name=Hotel_name):
                ext = "Data already exit"
                return render(request, 'updatehoteldetails.html', {'ext': ext})

            else:
                self_hotel.Hotel_name = Hotel_name
                self_hotel.save()
                return redirect('hotel_self_details')
        else:
            self_hotel = hotel_details.objects.get(id=pk)
            return render(request, 'updatehoteldetails.html', {'self_hotel': self_hotel})
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
