import json
import os
from django.contrib.auth import authenticate, login, logout

from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import random

from django.urls import reverse
from django.db.models import Q
from app_test.models import *
from django.contrib.auth.hashers import check_password, make_password

# index page


def indexpage(request):
    return render(request, 'index.html')


# hotel login

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        
           
        user = authenticate(username=username, password=password)


        if user:
            login(request, user)
            return redirect('adminHome')
       
        else:
            email_ext = hotel_details.objects.get(Email=username)
            if email_ext:
                pwd_valid = check_password(password, email_ext.Password)
                if pwd_valid:
                    request.session['id'] = email_ext.id
                    return redirect('hotelhome')
                else:
                    msg = "Password is incorrect"
                    return render(request, 'login.html', {'msg': msg})
            else:
                msg = "Not a user"
                return render(request, 'login.html', {'msg': msg})

    else:
        return render(request, 'login.html')


def admin_logout(request):
    logout(request)
    return redirect('login_page')

def adminHome(request):

    if request.user.is_authenticated:
        hotel_det = hotel_details.objects.all().order_by('?')
        return render(request, 'adminHome.html', {'hotel_det': hotel_det})
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

                pass1 = random.SystemRandom().randint(100000, 999999)
                print(pass1)
                password = make_password(str(pass1))

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

            if hotel_data.Hotel_name == hotel_name:
                hotel_data.Hotel_name = hotel_name
                hotel_data.Email = email
                hotel_data.Phone_number = request.POST.get('phone', None)
                hotel_data.Address = request.POST.get('address', None)
                hotel_data.save()
                msg = "Data update successfully"
                return render(request, 'updatehotel.html', {'msg': msg})

            else:
                if hotel_details.objects.filter(Q(Hotel_name=hotel_name) & ~Q(id=pk)):
                    exits = "Already exist"
                    return render(request, 'updatehotel.html', {'exits': exits})
                else:
                    hotel_data.Hotel_name = hotel_name
                    hotel_data.Email = email
                    hotel_data.Phone_number = request.POST.get('phone', None)
                    hotel_data.Address = request.POST.get('address', None)
                    hotel_data.save()
                    msg = "Data update successfully"
                    return render(request, 'updatehotel.html', {'msg': msg})

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
        return redirect('/')
    else:
        return redirect('/')


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
                msg = "Data updated successfully"
                return render(request, 'updatehoteldetails.html', {'msg': msg})
            
            else:

                if hotel_details.objects.filter(Q(Hotel_name=Hotel_name) & ~Q(id=pk)):
                    ext = "Data already exit"
                    return render(request, 'updatehoteldetails.html', {'ext': ext})

                else:
                    self_hotel.Hotel_name = Hotel_name
                    self_hotel.save()
                    msg = "Data updated successfully"
                    return render(request, 'updatehoteldetails.html', {'msg': msg})
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
