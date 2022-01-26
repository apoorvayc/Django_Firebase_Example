import pyrebase
from django.http import HttpResponse
import json

# Create your views here.
config = {
    'apiKey': 'AIzaSyCCYMDQ43IdFjxzkIdFPlwwyiSRiw0abSU',
    'authDomain': 'ctrldebthack.firebaseapp.com',
    'projectId': 'ctrldebthack',
    'storageBucket': 'ctrldebthack.appspot.com',
    'messagingSenderId': '231552560212',
    'appId': '1:231552560212:web:aacb5f70bc1ecb342951c1',
    'databaseURL':'https://ctrldebthack-default-rtdb.firebaseio.com/'
  }


firebase = pyrebase.initialize_app(config)
database = firebase.database()
print(database.child("Student_Registration").child("apoorvayc").get().val()["email"])