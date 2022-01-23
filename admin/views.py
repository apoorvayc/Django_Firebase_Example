from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
import json
import datetime
import pyrebase
from django.contrib.auth import authenticate

# Create your views here.
# Create your views here.
config = {
    'apiKey': "AIzaSyCCYMDQ43IdFjxzkIdFPlwwyiSRiw0abSU",
    'authDomain': "ctrldebthack.firebaseapp.com",
    'projectId': "ctrldebthack",
    'storageBucket': "ctrldebthack.appspot.com",
    'messagingSenderId': "231552560212",
    'appId': "1:231552560212:web:aacb5f70bc1ecb342951c1",
    'databaseURL':"https://ctrldebthack-default-rtdb.firebaseio.com/"
  }


firebase = pyrebase.initialize_app(config)
database = firebase.database()
authe = firebase.auth()

# Create your views here.

def ad_sign_in(request):
    if "uid" not in request.session.keys():
        request.session['uid'] = None
        request.session['email'] = None

    if request.session['uid'] != None:
        currentuserrid = request.session['email']
        print("Email ", currentuserrid)
        return render(request,"ad_dashboard.html")
    return render(request, "admin_signin.html")


def admin_post_signin(request):
    for key, value in request.POST.items():
        print('{} => {}'.format(key, value))
    if "uid" not in request.session.keys():
        request.session['uid'] = None
    if request.session['uid'] == None:
        if request.POST.get('email') == None or request.POST.get("password") == None:
            # return redirect('http://127.0.0.1:8000/')
            return HttpResponse("you are not signed in")
        request.session['email'] = request.POST.get('email')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:

            user = authe.sign_in_with_email_and_password(email, password)

            session_id = user['idToken']

            request.session['uid'] = session_id
            request.session['email1'] = email
            return render(request, "ad_dashboard.html")
        except:
            message = "Please check your emailID / Password"
            return render(request, "admin_signin.html", {"msg": message})

    else:
        return render(request, "ad_dashboard.html")


def ad_dashboard(request):
    return render(request, "ad_dashboard.html")

def add_admin(request) :
    email = "admin@gmail.com"
    password = "admin123"
    mail = email.split("@")[0]

    database.child("ADMIN").child(mail).set({"name": "Apoorva", "email" : email})
    return admin_post_signin(request)

def ad_logout(request):
    if "uid" in request.session.keys():
        if request.session['uid'] != None:
            request.session['uid'] = None
            request.session['email'] = None
        else:
            message = "user is not logged in"
            return render(request, "signIn.html")
        auth.logout(request)
    return render(request, 'admin_signin.html')


def stud_data(request):
    name =database.child("Student_Registration").get().val()
    x=[]

    return HttpResponse(json.dumps(name), content_type='application/json')

def vol_data(request):
    name =database.child("Volunteer_Registration").get().val()
    return HttpResponse(json.dumps(name), content_type='application/json')

def add_study_material(request) :
    if request.method == "POST" :
        url = request.POST["url"]
        url = url.replace("watch?v=","embed/")
        print(url)
        subject = request.POST['displayValue']
        database.child("Study_Material").child(subject).push({1:url})
    return render(request,"ad_dashboard.html")
    
def get_dash_data(request) :
    pairs = database.child("Connected_stud_vol").get().val()
    row = []
    for i in pairs :
        row.append([i.split("-")])
    return HttpResponse(json.dumps(row), content_type='application/json')

    
    