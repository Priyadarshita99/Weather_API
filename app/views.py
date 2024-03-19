from django.shortcuts import render

# Create your views here.

from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
import requests

def registration(request):
    UFO=UserForm()
    PFO=ProfileForm()
    d={'UFO':UFO,'PFO':PFO}
    if request.method=='POST' and request.FILES:
        UFD=UserForm(request.POST)
        PFD=ProfileForm(request.POST,request.FILES)

        if UFD.is_valid() and PFD.is_valid():
            MUFDO=UFD.save(commit=False)
            pw=UFD.cleaned_data['password']
            MUFDO.set_password(pw)                      #encryption
            MUFDO.save()

            MPFDO=PFD.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()

            send_mail(
                'Registration',
                'Registration is successful',
                'priyadarshita44@gmail.com',
                [MUFDO.email],
                fail_silently=False
            )
            return HttpResponse('Registration is successful')
        else:
            return HttpResponse('Invalid Data')
    return render(request,'registration.html',d)

def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Incorrect Username or Password.Please try again.')
    return render(request,'user_login.html')

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_profile(request):
    un=request.session.get('username')
    UO=User.objects.get(username=un)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_profile.html',d)

@login_required
def change_password(request):
    if request.method=='POST':
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        npw=request.POST['pw']
        UO.set_password(npw)
        UO.save()
        return HttpResponse('Password Changed Sucessfully')
    return render(request,'change_password.html')

def forgot_password(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']

        LUO=User.objects.filter(username=username)
        if LUO:
            UO=LUO[0]
            UO.set_password(password)
            UO.save()
            return HttpResponse('Reset password is done ')
        else:
            return HttpResponse('Username is not Valid')
    return render(request,'forgot_password.html')

@login_required
def search(request):
    if request.method=='POST':
        city_name=request.POST['city']
        api_key='f6d95bc7823abe365d8ca6012ca5547b'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
        response = requests.get(url)
        weather_data = response.json()
        print(weather_data)
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        weather=weather_data['main']['feels_like']
        speed=weather_data['wind']['speed']
        username=request.session.get('username')
        LUO=User.objects.get(username=username)
        obj=WeatherData.objects.get_or_create(username=LUO,city=city_name, temperature=temperature, humidity=humidity,weather=weather, speed=speed)[0]
        obj.save()
        d={'obj':obj}
        return render(request,'search.html',d) 
    return render(request,'search.html')

@login_required
def user_history(request):
    username=request.session['username']
    UO=User.objects.get(username=username)
    LWO=WeatherData.objects.filter(username=UO)

    d={'LWO':LWO}
    return render(request,'user_history.html',d)

def all_history(request):
    LWO=WeatherData.objects.all()
    d={'LWO':LWO}
    return render(request,'all_history.html',d)