from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
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
            user = authenticate(email="admin@gmail.com", password='admin')
            session_id = user['idToken']
            request.session['uid'] = session_id
            request.session['email1'] = email
            return render(request, "ad_dashboard.html")
        except:
            message = "Please check your emailID / Password"
            return render(request, "admin_signin.html", {"msg": message})




def ad_dashboard(request):
    return render(request, "ad_dashboard.html")

def add_admin(request) :
    email = "apoorvayc@gmail.com"
    password = "apoorva@123"
    mail = email.split("@")[0]

    database.child("ADMIN").child(mail).set({"name": "Apoorva", "email" : email})
    return admin_post_signin(request)