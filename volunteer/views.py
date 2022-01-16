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
# Create your views here.


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

def frontend_to_backend(request) :
	if request.method == "POST" :
		firstname = request.POST.get("fname")
		lastname = request.POST.get("lname")
		print(firstname,lastname)
		
	return render(request,"temp.html")
    

def vol_chat(request,name):
    name = name.split("@")
    student_email = name[0]
    student_sub = name[1]
    student_day = name[2]
    student_from = name[3]
    student_to = name[4]     
    volunteer_email = "anjalirc"
    return render(request,"vol_chat.html",{"student_email":student_email,"volunteer_email":volunteer_email,"student_sub":student_sub,"student_day":student_day,"student_from":student_from,"student_to":student_to})
    
    
def get_subject_wise_students(day,vol_category,subject) :
    student_obj = []
    for std in range(int(vol_category.split('-')[0]),int(vol_category.split('-')[1])+1,1) :
        student_obj.append(database.child("Student_Day").child(day).child(std).child(subject).get().val())
    return student_obj

def get_day_wise_student_pref(stud_email,day) :
    return database.child('Student_Availability').child(stud_email).child(day).get().val()
    
def match_vol_to_stud(request) :
    #get student details in function
    """
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
    """
    match_list = []
    #vol_std = "11-12"
    #write func for stud category 
    vol_category = "11-12"
    vol_email = "anjalirc"
    vol_subj_list = ["History","Geography"]
    vol_avail = {'Monday': {'from':'10','to':'13'},'Tuesday':{'from':'5','to':'8'},'Sunday': {'from':'12','to':'15'}}
    for i in vol_avail :
        day = i
        vol_fro = int(vol_avail[i]["from"])
        vol_to = int(vol_avail[i]["to"])
        print("Volunteer details")
        print(vol_email,day, vol_fro,vol_to)
        for j in vol_subj_list :
            subject = j
            print(subject)
            students = get_subject_wise_students(day,vol_category,subject)
            print(students)
            for stud in students :
                if stud :
                    print(stud,)
                    try :
                        tree = IntervalTree()
                        for s in stud :
                            stud_email = stud[s]["student"]
                            print(stud_email)
                            time = get_day_wise_student_pref(stud_email,day)
                            print(time)
                            fro = int(time["from"])
                            to = int(time["to"])
                            tree.addi(fro,to,stud_email)
                        overlap = tree.overlap(vol_fro,vol_to) 
                        print("Overlaps if any for studnets",overlap)
                        for t in overlap :
                            start = t[0] if t[0] > vol_fro else vol_fro
                            end = t[1] if t[1] < vol_to else vol_to
                            
                            match_str = t[2] + "@" + subject + "@" + day + "@" + str(start) + "@" + str(end)
                            
                            match_list.append(match_str.split("@"))
                            #match_list.append(check_for_overlaps(overlap,stud_fro,stud_to,stud_email,subject,day))
                    except :
                        continue
    
    return render(request,"vol_dash.html",{"email":vol_email,"match_list":match_list})
    
def messages(request,name) :
    current_email = name
    rec_msgs = database.child("Received_Messages").child(name).get().val()
    rec_msgs_list = []
    for i in rec_msgs :
        rec_msgs_list.append([i, rec_msgs[i]])
    return render(request,"vol_rec_msgs.html",{"rec_msgs_list":rec_msgs_list})
    
    