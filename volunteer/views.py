from django.shortcuts import render
from django.contrib import auth
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
authe = firebase.auth()

def vsign_in(request):
    if "uid" not in request.session.keys():
        request.session['uid'] = None
        request.session['email'] = None

    if request.session['uid'] != None:
        currentuserrid = request.session['email']
        print("Email ", currentuserrid)
        match_list = []
        vol_email = request.session['email'].split("@")[0]
        vol_category = database.child("Volunteer_Registration").child(vol_email).get().val()["grade"]
        vol_subj_list = database.child("Volunteer_Subject_Preference").child(vol_email).child("subject").get().val()
        vol_avail_data = database.child("Volunteer_Availability").child(vol_email).get().val()
        return render(request,"vol_dash.html")
    return render(request, "vsignin.html")

def vpost_signin(request):
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
        ename = email.split("@")[0]
        password = request.POST.get('password')
        try:
            user = authe.sign_in_with_email_and_password(email, password)
            session_id = user['idToken']
            request.session['uid'] = session_id
            request.session['email'] = email
            ename = request.session['email'].split("@")[0]
            name = database.child('Volunteer_Registration').get().val()
            for n in name:
                if ename == n:
                    newname = (name[n]["name"])
            match_list = []
            vol_email = request.session['email'].split("@")[0]
            vol_category = database.child("Volunteer_Registration").child(vol_email).get().val()["grade"]
            vol_subj_list = database.child("Volunteer_Subject_Preference").child(vol_email).child("subject").get().val()
            vol_avail_data = database.child("Volunteer_Availability").child(vol_email).get().val()
            return render(request,"vol_dash.html")

        except:
            message = "Invalid Credentials!!"
            return render(request, "vsignin.html", {"msg": message})

    else:
        ename = request.session['email'].split("@")[0]
        name = database.child('Volunteer_Registration').get().val()
        for n in name:
            if ename == n:
                newname = (name[n]["name"])

        match_list = []
        vol_email = request.session['email'].split("@")[0]
        vol_category = database.child("Volunteer_Registration").child(vol_email).get().val()["grade"]
        vol_subj_list = database.child("Volunteer_Subject_Preference").child(vol_email).child("subject").get().val()
        vol_avail_data = database.child("Volunteer_Availability").child(vol_email).get().val()
        return render(request,"vol_dash.html")


def vsign_up(request):

    return render(request, "vsignup.html")


def vinfo(request):
    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        sname = email.split("@")[0]
        password = request.POST.get('password')
        # grade
        grade = request.POST.get('displayValue')
        print(grade)
        # subject
        subject = request.POST.getlist('check')
        print(subject)

        try:
            user = authe.create_user_with_email_and_password(email, password)
        except:
            message = "Unable to create Account. Try Again!!"
            return render(request, "vsignup.html", {"msg": message})
        request.session["email"] = email
        database.child("Volunteer_Registration").child(sname).set({"name": name, "grade": grade})
        database.child("Volunteer_Subject_Preference").child(sname).set({"subject": subject})

    return render(request, "vinfo.html",{"refresh":"0"})


def vpost_signup(request):
    if request.method == "POST":

        email = request.session["email"]
        sname = email.split("@")[0]

        # availability
        dayvalue = request.POST.get('dayValue')
        fromvalue = request.POST.get('fromtime')
        tovalue = request.POST.get('totime')

        database.child("Volunteer_Availability").child(sname).child(dayvalue).push({"from": fromvalue, "to": tovalue})

        return render(request, "vinfo.html", {"refresh":"1"})
    #return render(request, "vdashboard.html", {"n": name})

def vlogout(request):
    if "uid" in request.session.keys():
        if request.session['uid'] != None:
            request.session['uid'] = None
            request.session['email'] = None
        else:
            message = "user is not logged in"
            return render(request, "vsignin.html")
        auth.logout(request)
    return render(request, 'vsignin.html')

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
    match_list = []
    vol_email = request.session['email'].split("@")[0]
    vol_category = database.child("Volunteer_Registration").child(vol_email).get().val()["grade"]
    vol_subj_list = database.child("Volunteer_Subject_Preference").child(vol_email).child("subject").get().val()
    vol_avail_data = database.child("Volunteer_Availability").child(vol_email).get().val()
       
    for i in vol_avail_data :
        day = i
        for j in vol_avail_data[i] :
            time_from = vol_avail_data[i][j]["from"]
            time_to = vol_avail_data[i][j]["to"]
            for sub in vol_subj_list :        
                try :
                    database.child("Day").child(day).child(vol_category).child(sub).update({vol_email:"1"})
                except :
                    database.child("Day").child(day).child(vol_category).child(sub).update({vol_email:"1"})
                
    return render(request,"vol_dash.html")
"""


    
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
 """   
def messages(request,name) :
    current_email = name
    rec_msgs = database.child("Received_Messages").child(name).get().val()
    rec_msgs_list = []
    for i in rec_msgs :
        rec_msgs_list.append([i, rec_msgs[i]])
    return render(request,"vol_rec_msgs.html",{"rec_msgs_list":rec_msgs_list})
    
def confirm_stud_vol(request) :
    student_email = request.GET["student_email"]
    student_sub = request.GET["student_sub"]
    student_day = request.GET["student_day"]
    student_from = request.GET["student_from"]
    student_to = request.GET["student_to"]
    volunteer_email = "anjalirc"
    time = database.child("Volunteer_Availability").child(volunteer_email).child(student_day).get().val()
     
        
    
    return HttpResponse("Done")
    