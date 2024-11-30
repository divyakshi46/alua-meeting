import requests
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
import os
# Create your views here.

def index(request):
    return render(request,'index.html')


def vcapi(request):
    return render(request,'vcapi.html')

def joinroom(request):
    if request.method =='POST':
        roomID = request.POST['roomID']
        return redirect('vcapi?roomID='+roomID)
    return render(request ,'join.html')

def register(request):
    if request.method=='POST':
        username= request.POST['username']
        email= request.POST['email']
        password= request.POST['password']
        password2= request.POST['password2']
        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already exists')
                return  redirect('register')
            elif User.objects.filter(username=username).exists():
                 messages.info(request,'Username already exists')
                 return  redirect('register')
            else:

                user=User.objects.create_user(username=username,email=email,password=password2)
                user.save()
                return redirect('login')
        else:
             messages.info(request,'Password enter is not same')
             return  redirect('register')
    else:
        return render(request,'register.html')

            

def login(request):
    if request.method=='POST':
         username= request.POST['username']
         password= request.POST['password']
         user=auth.authenticate(username=username,password=password)
         if user is not None:
             auth.login(request,user)
             return redirect('/')
         else:
             messages.info(request,'Credentials are incorrect')
             return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')   




def counter(request):
    text=request.POST['text']
    amount_of_word=len(text.split())
    return render(request,'counter.html',{'amount':amount_of_word})

def contact(request):
    return render(request,'contact.html')

def support(request):
    return render(request,'support.html')

def blog(request):
    return render(request,'blog.html')


#Fetch the API_KEY from environment variables
API_KEY = os.getenv("API_KEY")

def meeting_view(request): # pass the room id from teh frontend
    url = "https://api.digitalsamba.com/api/v1/rooms/"

    
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    response = requests.get(url, headers=headers)

    # print(response.json())
    
    if response.status_code == 200:
        data = response.json()

        # filter out the room
        # room_url = data["data"].filter(id == request.id)["room_url"]
        room_url = data["data"][1]["room_url"]
        return redirect(room_url)
    else:
        print(response.status_code)
        return render(request, "error_page.html", {"error": "Failed to load the meeting. Please try again later."})
    