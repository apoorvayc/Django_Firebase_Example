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
"""
# Create your tests here.
vol_reg_data = {
    'adityarc':{'name':'Aditya', 'grade':'5-7'},
    'apoorvayc':{'name':'Apoorva', 'grade':'5-7'},
    'anjalirc':{'name':'Anjali', 'grade':'11-12'},
    'bhagyeshjc':{'name':'Bhagyesh', 'grade':'8-10'},
    'rutujapc':{'name':'Rutuja', 'grade':'11-12'},
    'ompc':{'name':'Om', 'grade':'11-12'},
    'aayushmc':{'name':'Aayush', 'grade':'11-12'},
    'kartikimc':{'name':'Kartiki', 'grade':'5-7'},
    'tanayrc':{'name':'Tanay', 'grade':'5-7'},
    'chinmayirc':{'name':'Chinmayi', 'grade':'8-10'}
    }
database.child('Volunteer_Registration').set(vol_reg_data)

vol_avail_data = {
    'adityarc':
        {
        'Monday': {
                    'from':'8',
                    'to':'11'	
                    },
        'Tuesday':{
            'from':'5',
            'to':'8'	
            }
        }
    ,
    'apoorvayc':
        {
        'Monday': {
                    'from':'9',
                    'to':'12'	
                    },
        'Tuesday':{
            'from':'10',
            'to':'15'	
            }
        }
    ,
    'anjalirc':
        {
        'Monday': {
                    'from':'10',
                    'to':'13'	
                    },
        'Tuesday':{
            'from':'5',
            'to':'8'	
            },
        'Sunday': {
                    'from':'12',
                    'to':'15'	
                    }
            
        }
    ,
    'bhagyeshjc':
        {
        'Monday': {
                    'from':'9',
                    'to':'17'	
                    },
        'Tuesday':{
            'from':'5',
            'to':'8'	
            }
        }
    ,
    'rutujapc':
        {
        'Monday': {
                    'from':'12',
                    'to':'15'	
                    },
        'Tuesday':{
            'from':'5',
            'to':'8'	
            }
        }
    ,
    'ompc':
        {
        'Monday': {
                    'from':'13',
                    'to':'16'	
                    },
        'Tuesday':{
            'from':'5',
            'to':'8'	
            }
        }
    ,
    'aayushmc':
        {
        'Monday': {
                    'from':'14',
                    'to':'17'	
                    },
        'Tuesday':{
            'from':'5',
            'to':'8'	
            }
        }
    ,
    'kartikimc':
        {
        'Monday': {
                    'from':'15',
                    'to':'18'	
                    },
        'Tuesday':{
            'from':'5',
            'to':'8'	
            }
        }
    ,
    'tanayrc':
        {
        'Monday': {
                    'from':'16',
                    'to':'19'	
                    },
        'Tuesday':{
            'from':'5',
            'to':'8'	
            }
        }
    ,
    'chinmayirc':
        {
        'Monday': {
                    'from':'9',
                    'to':'17'	
                    },
        'Tuesday':{
            'from':'5',
            'to':'8'	
            }
        }
    
}
database.child('Volunteer_Availability').set(vol_avail_data)
vol_subj_data = {
    'adityarc':{'1':'Maths','2':'Science'},
    'apoorvayc':{'1':'English','2':'Hindi'},
    'anjalirc':{'1':'History','2':'Geography'},
    'bhagyeshjc':{'1':'Maths','2':'Marathi'},
    'rutujapc':{'1':'Maths-Algebra','2':'English-Grammar'},
    'ompc':{'1':'Maths','2':'Science'},
    'aayushmc':{'1':'English','2':'Hindi'},
    'kartikimc':{'1':'History','2':'Geography'},
    'tanayrc':{'1':'Sanskrit','2':'Marathi'},
    'chinmayirc':{'1':'Maths-Geometry','2':'Science'}
}
database.child('Volunteer_Subject_Preference').set(vol_subj_data)

for i in vol_avail_data :
    email = i
    print(email)
    vol_grade_details = database.child("Volunteer_Registration").child(email).get().val()
    vol_grade = vol_grade_details["grade"]
    print(vol_grade)
    day_time = vol_avail_data[i]
    for j in day_time :
        day = j
        time = day_time[j]
        time_from = time["from"]
        time_to = time["to"]
        vol_subj_details = database.child("Volunteer_Subject_Preference").child(email).get().val()
        print(vol_subj_details)
        for sub in vol_subj_details[1:] :        
            database.child("Day").child(day).child(vol_grade).child(sub).push({"volunteer":email})
"""

database.child("dummy").child("child1").set({"child2":"val2","child3":"val3"})

database.child("dummy").child("child1").child("child2").remove()
