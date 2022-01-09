from django.shortcuts import render
import pyrebase
from django.http import HttpResponse
from intervaltree import Interval, IntervalTree

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

def reg_student():
	#email, password, name, std, subj, day, time

def login_stud():
	#email, password



def add_student(request) :
	email = "apoorvayc@gmail.com"
	email = email.split("@")[0]
	std = "6"
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

def get_subject_wise_volunteers(day,stud_category,subject) :
	return database.child("Day").child(day).child(stud_category).child(subject).get().val()

def get_day_wise_volunteer_pref(vol_email,day) :
	return database.child('Volunteer_Availability').child(vol_email).child(day).get().val()

def check_for_overlaps(overlap,stud_fro,stud_to,stud_email,subject,day) :
	for t in overlap :
		start = t[0] if t[0] > stud_fro else stud_fro
		end = t[1] if t[1] < stud_to else stud_to
		print(t[2]," is matched with -", stud_email, "for", subject, "on",day, "from time", start,"to",end)

def match_stud_to_vol(request) :
	#get student details in function
	stud_std = "6"
	stud_category = "5-7"
	stud_email = "apoorvayc"
	stud_subj_list = ["English","Maths"]
	stud_avail = {
						"Monday": {
									"from":"7",
									"to":"10"	
									},
						"Tuesday":{
							"from":"18",
							"to":"19"	
							}
				}
	for i in stud_avail :
		day = i
		stud_fro = int(stud_avail[i]["from"])
		stud_to = int(stud_avail[i]["to"])
		# print("Day-",day)
		# print("Time-",stud_fro,"-",stud_to)
		for j in stud_subj_list :
			subject = j
			volunteers = get_subject_wise_volunteers(day,stud_category,subject)
			try :
				tree = IntervalTree()
				for v in volunteers :
					vol_email = volunteers[v]["volunteer"]
					time = get_day_wise_volunteer_pref(vol_email,day)
					fro = int(time["from"])
					to = int(time["to"])
					tree.addi(fro,to,vol_email)
				overlap = tree.overlap(stud_fro,stud_to) 
				check_for_overlaps(overlap,stud_fro,stud_to,stud_email,subject,day)
			except :
				continue

	return HttpResponse("Done")

