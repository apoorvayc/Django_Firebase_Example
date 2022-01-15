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
# Create your tests here.
stud_reg_data = {
    "riteshgc":{"name":"Ritesh","grade":"7"},
    "diptejjc":{"name":"Diptej","grade":"9"},
    "rupalimc":{"name":"Rupali","grade":"11"}
}
database.child("Student_Registration").set(stud_reg_data)
stud_avail_data = {
    "riteshgc":{"Monday":{"from":"10","to":"12"},"Tuesday":{"from":"10","to":"12"}},
    "diptejjc":{"Wednesday":{"from":"16","to":"20"},"Thursday":{"from":"16","to":"20"}},
    "rupalimc":{"Sunday":{"from":"13","to":"16"},"Saturday":{"from":"13","to":"16"}}    
}
database.child("Student_Availability").set(stud_avail_data)
stud_subj_data = {
    "riteshgc":{"1":"English","2":"Maths"},
    "diptejjc":{"1":"English-Grammar","2":"Maths-Algebra"},
    "rupalimc":{"1":"Hindi","2":"History","3":"Geography"}
}
database.child("Student_Subject_Preference").set(stud_subj_data)
