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

def sign_in(request):
    if "uid" not in request.session.keys():
        request.session['uid'] = None
        request.session['email'] = None

    if request.session['uid'] != None:
        currentuserrid = request.session['email']
        print("Email ", currentuserrid)
        return match_stud_to_vol(request)
    return render(request, "signIn.html")

def post_signin(request):
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
            request.session['email'] = email
            return match_stud_to_vol(request)

        except:
            message = "Please check your emailID / Password"
            return render(request, "signIn.html", {"msg": message})

    else:
        return match_stud_to_vol(request)
        
def sign_up(request):

    return render(request, "signUp.html")


def sinfo(request):
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
            return render(request, "signUp.html", {"msg": message})
        request.session["email"] = email
        database.child('Student_Registration').child(sname).set({"name": name, "grade": grade})
        database.child("Student_Subject_Preference").child(sname).set({"subject": subject})

    return render(request, "sinfo.html", {"refresh": "0"})


def post_signup(request):
    if request.method == "POST":

        email = request.session["email"]
        sname = email.split("@")[0]

        # availability
        dayvalue = request.POST.get('dayValue')
        fromvalue = request.POST.get('fromtime')
        tovalue = request.POST.get('totime')

        database.child('Student_Availability').child(sname).child(dayvalue).push({"from": fromvalue, "to": tovalue})

        return render(request, "sinfo.html", {"refresh":"1"})
    return render(request, "sinfo.html", {"refresh":"0"})
    #return render(request, "sdashboard.html", {"n": name})
def logout(request):
    if "uid" in request.session.keys():
        if request.session['uid'] != None:
            request.session['uid'] = None
            request.session['email'] = None
        else:
            message = "user is not logged in"
            return render(request, "signIn.html")
        auth.logout(request)
    return render(request, 'signIn.html')

def get_subject_wise_volunteers(day,stud_category,subject) :
    return database.child("Day").child(day).child(stud_category).child(subject).get().val()

def get_day_wise_volunteer_pref(vol_email,day) :
    return database.child('Volunteer_Availability').child(vol_email).child(day).get().val()

def get_student_category(stud_grade) :
    student_category = {"5":"5-7","6":"5-7","7":"5-7","8":"8-10","9":"8-10","10":"8-10","11":"11-12","12":"11-12"}
    return student_category[stud_grade]

def get_time_in_minutes(time) :
    return int(time.split(":")[0])*60+int(time.split(":")[1])
    
def match_stud_to_vol(request) :
    match_list = []
    stud_email = request.session['email'].split("@")[0]
    stud_grade = database.child("Student_Registration").child(stud_email).get().val()["grade"]
    stud_category = get_student_category(stud_grade)
    stud_subj_list = database.child("Student_Subject_Preference").child(stud_email).child("subject").get().val()
    stud_avail_data = database.child("Student_Availability").child(stud_email).get().val()
    
    #day loop
    for i in stud_avail_data :
        day = i
        for j in stud_avail_data[i] :
            time_from = stud_avail_data[i][j]["from"]
            stud_fro = get_time_in_minutes(time_from)
            time_to = stud_avail_data[i][j]["to"]
            stud_to = get_time_in_minutes(time_to)
            #subject loop 
            for sub in stud_subj_list :
                emails = database.child("Student_Day").child(day).child(stud_grade).child(sub).get().val()
                try :
                    if stud_email not in emails.keys :
                        database.child("Student_Day").child(day).child(stud_grade).child(sub).update({stud_email:"1"})
                except :
                        database.child("Student_Day").child(day).child(stud_grade).child(sub).set({stud_email:"1"})
                #get volunteers filtered by day,std and subject
                volunteers = get_subject_wise_volunteers(day,stud_category,sub)
                try :
                    tree = IntervalTree()
                    for v in volunteers.keys() :
                        vol_email = v

                        #get filtered volunteers time preferences 
                        time = get_day_wise_volunteer_pref(vol_email,day)
                        print(time)
                        for t in time :
                            fro = get_time_in_minutes(time[t]["from"])
                            to = get_time_in_minutes(time[t]["to"])
                            tree.addi(fro,to,vol_email)
                    #check for overlapping time intervals between volunteers and student 
                    overlap = tree.overlap(stud_fro,stud_to) 
                    print("Overlaps if any for volunters",overlap)
                    for t in overlap :
                        start = t[0] if t[0] > stud_fro else stud_fro
                        end = t[1] if t[1] < stud_to else stud_to
                        start_hr = str(start//60).zfill(2)
                        start_min = str(start%60).zfill(2)
                        end_hr = str(end//60).zfill(2)
                        end_min = str(end%60).zfill(2)
                        
                        match_str = t[2] + "@" + sub + "@" + day + "@" + str(start_hr)+":"+str(start_min) + "@" + str(end_hr)+":"+str(end_min)
                        
                        match_list.append(match_str.split("@"))
                except :
                    continue
    
    return render(request,"stud_dash.html",{"email":stud_email,"match_list":match_list})

def stud_chat(request,name):
    name = name.split("@")
    volunteer_email = name[0]
    volunter_sub = name[1]
    volunter_day = name[2]
    volunter_from = name[3]
    volunter_to = name[4]     
    student_email = request.session["email"].split("@")[0]
    return render(request,"stud_chat.html",{"student_email":student_email,"volunteer_email":volunteer_email,"volunteer_sub":volunter_sub,"volunteer_day":volunter_day,"volunteer_from":volunter_from,"volunteer_to":volunter_to})
    
def messages(request,name) :
    current_email = name
    rec_msgs = database.child("Received_Messages").child(name).get().val()
    rec_msgs_list = []
    for i in rec_msgs :
        rec_msgs_list.append([i, rec_msgs[i]["subj"], rec_msgs[i]["day"], rec_msgs[i]["from"], rec_msgs[i]["to"], rec_msgs[i]["msg"]])
    return render(request,"stud_rec_msgs.html",{"rec_msgs_list":rec_msgs_list})

