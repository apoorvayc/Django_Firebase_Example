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
# Create your views here.
def reg_volunteer():
	#email, password, name, std, subj, day, time

def login_volunteer():
	#email, password

def add_volunteer(request) :
	email = "adityarc@gmail.com"
	email = email.split("@")[0]
	
	database.child("Volunteer_Reg").child(email).set(
										{"name":"Aditya"}
									)
	database.child("Volunteer_Availability").child(email).set(
										{
														"Monday": {
																	"from":"8",
																	"to":"12"	
																	},
														"Tuesday":{
															"from":"5",
															"to":"8"	
															}
														}

									) 
	database.child("Volunteer_Subject_List").child(email).set(
											{
													"1":"Maths",
													"2":"Science"
											}

		)
	return HttpResponse("Done")


def temp_func(request) :
	database.child("Day").child("Monday").child("5-7").child("Maths").push({"volunteer":"adityarc"})
	database.child("Day").child("Monday").child("5-7").child("Science").push({"volunteer":"adityarc"	})
	database.child("Day").child("Tuesday").child("5-7").child("Maths").push({"volunteer":"adityarc"})
	database.child("Day").child("Tuesday").child("5-7").child("Science").push({"volunteer":"adityarc"})	
	database.child("Day").child("Tuesday").child("5-7").child("Maths").push({"volunteer":"rutujapc"})
	database.child("Day").child("Tuesday").child("5-7").child("English").push({"volunteer":"rutujapc"})
	database.child("Day").child("Wednesday").child("5-7").child("Maths").push({"volunteer":"rutujapc"})
	database.child("Day").child("Wednesday").child("5-7").child("English").push({"volunteer":"rutujapc"})													
	return HttpResponse("Done")
