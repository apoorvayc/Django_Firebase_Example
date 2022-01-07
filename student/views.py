from django.shortcuts import render
import pyrebase
from django.http import HttpResponse

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

def add_student(request) :
	email = "apoorvayc@gmail.com"
	email = email.split("@")[0]
	
	database.child("Student_Reg").set(
										{	
											email : {"name":"Apoorva"}
										}
									)
	database.child("Student_Availability").set(
										{	
											email : {
														"Monday": {
																	"from":"7",
																	"to":"10"	
																	},
														"Tuesday":{
															"from":"7",
															"to":"10"	
															}
														}

										}
									) 
	database.child("Student_Subject_List").set(
											{ email: {
													"1":"Maths",
													"2":"Science"
											}
										}
		)
	return HttpResponse("Done")

