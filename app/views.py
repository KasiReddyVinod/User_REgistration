from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
from app.forms import *
from app.models import *
from django.http import HttpResponse
def registration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}

    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            NSUO=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            NSUO.set_password(password)
            NSUO.save()

            NSPO=pfd.save(commit=False)
            NSPO.username=NSUO
            NSPO.save()

            send_mail('User Registration',
                      "Registration successfully",
                      'enfield748@gmail.com',
                      [NSUO.email],
                      fail_silently=False)

    


            return HttpResponse('Regsitration is Susssessfulll')
        else:
            return HttpResponse('Not valid')
    return render(request,'registration.html',d)
def home_page(request):
    return render(request,'home.html')



def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home_page'))
        else:
            return HttpResponse('Invalid username or password') 
        
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_page'))

@login_required
def display_profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render (request,'display_profile.html',d)

@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['pw']
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('Password Changed Successfully')
    return render(request,'change_password.html')


def forgot_password(request):
    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']
        LUO=User.objects.filter(username=un)
        if LUO:
            LUO[0].set_password(pw)
            LUO[0].save()
            return HttpResponse('Password Reset Done')
        else:
            return HttpResponse('Entered Data not Availabe')
    return render (request,'forgot_password.html')