from django.shortcuts import render
from django.contrib import auth
import pyrebase
from django.http import HttpResponse
from intervaltree import Interval, IntervalTree
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import json

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
        email = request.session['email']
        sname = database.child("Volunteer_Registration").child(email.split("@")[0].replace(".",",")).get().val()["name"]
        return render(request,"vol_dash.html",{"name":sname})

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
        ename = email.split("@")[0].replace(".",",")
        password = request.POST.get('password')
        try:
            user = authe.sign_in_with_email_and_password(email, password)
            session_id = user['idToken']
            request.session['uid'] = session_id
            request.session['email'] = email
            sname = database.child("Volunteer_Registration").child(email.split("@")[0].replace(".",",")).get().val()["name"]
            return render(request,"vol_dash.html",{"name":sname})

        except:
            message = "Invalid Credentials!!"
            return render(request, "vsignin.html", {"msg": message})

    else:
        email = request.session['email']
        sname = database.child("Volunteer_Registration").child(email.split("@")[0].replace(".",",")).get().val()["name"]
        return render(request,"vol_dash.html",{"name":sname})


def vsign_up(request):

    return render(request, "vsignup.html")


def vinfo(request):
    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        sname = email.split("@")[0].replace(".",",")
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
        session_id = user['idToken']
        request.session['uid'] = session_id
        database.child("Volunteer_Registration").child(sname).set({"name": name, "grade": grade, "email":email})
        database.child("Volunteer_Subject_Preference").child(sname).set({"subject": subject})

    return render(request, "vinfo.html",{"refresh":"0"})


def vpost_signup(request):
    if request.method == "POST":

        email = request.session["email"]
        sname = email.split("@")[0].replace(".",",")

        # availability
        dayvalue = request.POST.get('dayValue')
        fromvalue = request.POST.get('fromtime')
        tovalue = request.POST.get('totime')

        database.child("Volunteer_Availability").child(sname).child(dayvalue).push({"from": fromvalue, "to": tovalue})

        vol_email = request.session['email'].split("@")[0].replace(".",",")
        vol_category = database.child("Volunteer_Registration").child(vol_email).get().val()["grade"]
        vol_subj_list = database.child("Volunteer_Subject_Preference").child(vol_email).child("subject").get().val()
        vol_fro = get_time_in_minutes(fromvalue)
        vol_to = get_time_in_minutes(tovalue)
        for sub in vol_subj_list : 
            emails = database.child("Day").child(dayvalue).child(vol_category).child(sub).get().val()
            database.child("Day").child(dayvalue).child(vol_category).child(sub).update({vol_email:"1"})
               
        return render(request, "vinfo.html", {"refresh":"1"})
    return render(request, "vinfo.html", {"refresh":"0"})
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

def vol_chat(request,name):
    name = name.split("@")
    student_email = name[0]
    student_sub = name[1]
    student_day = name[2]
    student_from = name[3]
    student_to = name[4]     
    volunteer_email = request.session['email'].split("@")[0].replace(".",",")
    volunteer_name = database.child("Volunteer_Registration").child(volunteer_email).get().val()["name"]
    student_name = database.child("Student_Registration").child(student_email).get().val()["name"]
    return render(request,"vol_chat.html",{"student_email":student_email,"volunteer_email":volunteer_email,"student_sub":student_sub,"student_day":student_day,"student_from":student_from,"student_to":student_to,"volunteer_name":volunteer_name,"student_name":student_name})
    
def vdashboard(request) :
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
        ename = email.split("@")[0].replace(".",",")
        password = request.POST.get('password')
        try:
            user = authe.sign_in_with_email_and_password(email, password)
            session_id = user['idToken']
            request.session['uid'] = session_id
            request.session['email'] = email
            sname = database.child("Volunteer_Registration").child(email.split("@")[0].replace(".",",")).get().val()["name"]
            return render(request,"vol_dash.html",{"name":sname})

        except:
            message = "Invalid Credentials!!"
            return render(request, "vsignin.html", {"msg": message})

    else:
        email = request.session['email']
        sname = database.child("Volunteer_Registration").child(email.split("@")[0].replace(".",",")).get().val()["name"]
        return render(request,"vol_dash.html",{"name":sname})

    
def get_subject_wise_students(day,vol_category,subject) :
    student_obj = []
    for std in range(int(vol_category.split('-')[0]),int(vol_category.split('-')[1])+1,1) :
        student_obj.append(database.child("Student_Day").child(day).child(std).child(subject).get().val())
    return student_obj

def get_day_wise_student_pref(stud_email,day) :
    return database.child('Student_Availability').child(stud_email).child(day).get().val()
 

def get_time_in_minutes(time) :
    return int(time.split(":")[0])*60+int(time.split(":")[1])
     
def vol_dash_data(request) :
    match_list = []
    vol_email = request.session['email'].split("@")[0].replace(".",",")
    vname = database.child("Volunteer_Registration").child(vol_email).get().val()["name"]
    vol_category = database.child("Volunteer_Registration").child(vol_email).get().val()["grade"]
    vol_subj_list = database.child("Volunteer_Subject_Preference").child(vol_email).child("subject").get().val()
    vol_avail_data = database.child("Volunteer_Availability").child(vol_email).get().val()
    #day loop   
    for i in vol_avail_data :
        day = i
        print(day)
        for j in vol_avail_data[i] : 
            time_from = vol_avail_data[i][j]["from"]
            vol_fro = get_time_in_minutes(time_from)
            time_to = vol_avail_data[i][j]["to"]
            vol_to = get_time_in_minutes(time_to)
            #subject loop
            for sub in vol_subj_list : 
                emails = database.child("Day").child(day).child(vol_category).child(sub).get().val()
                database.child("Day").child(day).child(vol_category).child(sub).update({vol_email:"1"})
                #get students filtered by day,std and subject  
                students = get_subject_wise_students(day,vol_category,sub)
                for stud in students :
                    if stud :
                        try :
                            tree = IntervalTree()
                            for s in stud.keys() :
                                stud_email = s
                                #get filtered students time preferences  
                                time = get_day_wise_student_pref(stud_email,day)
                                for t in time :
                                    fro = get_time_in_minutes(time[t]["from"])
                                    to = get_time_in_minutes(time[t]["to"])
                                    tree.addi(fro,to,stud_email)
                            overlap = tree.overlap(vol_fro,vol_to) 
                            print("Overlaps if any for students",overlap)
                            for t in overlap :
                                start = t[0] if t[0] > vol_fro else vol_fro
                                end = t[1] if t[1] < vol_to else vol_to
                                start_hr = str(start//60).zfill(2)
                                start_min = str(start%60).zfill(2)
                                end_hr = str(end//60).zfill(2)
                                end_min = str(end%60).zfill(2)

                                match_str = t[2] + "@" + sub + "@" + day + "@" + str(start_hr)+":"+str(start_min) + "@" + str(end_hr)+":"+str(end_min) + "@" + vname
                                
                                match_list.append(match_str.split("@"))
                                #match_list.append(check_for_overlaps(overlap,stud_fro,stud_to,stud_email,subject,day))
                        except :
                            continue
   
    if match_list :
        match_list = sorted(match_list,key = lambda x : x[0])
    return HttpResponse(json.dumps(match_list), content_type='application/json')
 
def messages(request,name) :
    current_email = name
    rec_msgs = database.child("Received_Messages").child(name).get().val()
    rec_msgs_list = []
    for i in rec_msgs :
        rec_msgs_list.append([i, rec_msgs[i]["subj"], rec_msgs[i]["day"], rec_msgs[i]["from"], rec_msgs[i]["to"], rec_msgs[i]["msg"]])
    return render(request,"vol_rec_msgs.html",{"rec_msgs_list":rec_msgs_list})
    
def confirm_stud_vol(request) :
    
    student_email = request.GET["student_email"]
    student_sub = request.GET["student_sub"]
    student_day = request.GET["student_day"]
    student_from = request.GET["student_from"]
    student_to = request.GET["student_to"]
    volunteer_email = request.session['email'].split("@")[0].replace(".",",")
    """
    #update volunteer preferences
    time = database.child("Volunteer_Availability").child(volunteer_email).child(student_day).get().val()
    for t in time :
        tree = IntervalTree()
        tree.addi(get_time_in_minutes(time[t]["from"]),get_time_in_minutes(time[t]["to"]))
        overlap = tree.overlap(get_time_in_minutes(student_from), get_time_in_minutes(student_to)) 
        if overlap :
            if (get_time_in_minutes(time[t]["from"]) == get_time_in_minutes(student_from) and get_time_in_minutes(time[t]["to"]) == get_time_in_minutes(student_to)) :
                database.child("Volunteer_Availability").child(volunteer_email).child(student_day).child(t).remove()
            else :
                if get_time_in_minutes(time[t]["from"]) < get_time_in_minutes(student_from) :
                    database.child("Volunteer_Availability").child(volunteer_email).child(student_day).child(t).remove()
                    database.child("Volunteer_Availability").child(volunteer_email).child(student_day).push({"from":time[t]["from"],"to":student_from})
                if get_time_in_minutes(time[t]["to"]) > get_time_in_minutes(student_to) :
                    try :
                        database.child("Volunteer_Availability").child(volunteer_email).child(student_day).child(t).remove()
                    except :
                        pass
                    database.child("Volunteer_Availability").child(volunteer_email).child(student_day).push({"from":student_to, "to":time[t]["to"]})

            times = database.child("Volunteer_Availability").child(volunteer_email).child(student_day).get().val()
            try :
                if volunteer_email not in times.keys :
                    vol_category = database.child("Volunteer_Registration").child(volunteer_email).get().val()["grade"]
                    try :
                        database.child("Day").child(student_day).child(vol_category).child(student_sub).child(volunteer_email).remove()
                    except :
                        pass
            except :
                    pass
    
    #update student preferences
    time = database.child("Student_Availability").child(student_email).child(student_day).get().val()
    for t in time :
        tree = IntervalTree()
        tree.addi(get_time_in_minutes(time[t]["from"]),get_time_in_minutes(time[t]["to"]))
        overlap = tree.overlap(get_time_in_minutes(student_from),get_time_in_minutes(student_to)) 
        if overlap :
            if (get_time_in_minutes(time[t]["from"]) == get_time_in_minutes(student_from) and get_time_in_minutes(time[t]["to"]) == get_time_in_minutes(student_to)) :
                database.child("Student_Availability").child(student_email).child(student_day).child(t).remove()
            else :
                if get_time_in_minutes(time[t]["from"]) < get_time_in_minutes(student_from) :
                    database.child("Student_Availability").child(student_email).child(student_day).child(t).remove()
                    database.child("Student_Availability").child(student_email).child(student_day).push({"from":time[t]["from"],"to":student_from})
                if get_time_in_minutes(time[t]["to"]) > get_time_in_minutes(student_to) :
                    try :
                        database.child("Student_Availability").child(student_email).child(student_day).child(t).remove()
                    except :
                        pass
                    database.child("Student_Availability").child(student_email).child(student_day).push({"from":student_to,"to":time[t]["to"]})
            
            times = database.child("Student_Availability").child(student_email).child(student_day).get().val()
            try :
                if student_email not in times.keys :
                    stud_grade = database.child("Student_Registration").child(student_email).get().val()["grade"]
                    try :
                        database.child("Student_Day").child(student_day).child(stud_grade).child(student_sub).child(student_email).remove()
                    except :
                        pass
            except :
                    pass
    
    
    """
    database.child("Connected_stud_vol").child(student_email + "-" + volunteer_email + "-" + student_sub + "-" + student_day + "-" + student_from + "-" + student_to).set({"status":"confirmed"})
    mail_subj = "Volunteer: "+volunteer_email+" has confirmed to teach you"

    merge_data = {
        "student_sub":student_sub,
        "student_day":student_day,
        "student_from":student_from,
        "student_to":student_to,
        "volunteer_email":volunteer_email
    }
    html_body = render_to_string("temp.html", merge_data)
    email = database.child("Student_Registration").child(student_email).get().val()["email"]
    message = EmailMultiAlternatives(
       subject=mail_subj,
       body="",
       from_email="rutuom.12@gmail.com", 
       to=[email]
    )
    message.attach_alternative(html_body, "text/html")
    message.send(fail_silently=False)
    
    
    return HttpResponse("Done")

def vol_get_messages(request) :
    volunteer_email = request.session["email"].split("@")[0].replace(".",",")
    rec_msgs = database.child("Received_Messages").child(volunteer_email).get().val()
    rec_msgs_list = []
    try :
        for i in rec_msgs :
            rec_msgs_list.append([i, rec_msgs[i]["subj"], rec_msgs[i]["day"], rec_msgs[i]["from"], rec_msgs[i]["to"], rec_msgs[i]["msg"]])
    except :
        pass
    return HttpResponse(json.dumps(rec_msgs_list), content_type='application/json')
    
def get_connected_stud(request) :
    volunteer_email = request.session["email"].split("@")[0].replace(".",",")
    pairs = database.child("Connected_stud_vol").get().val()
    row = []
    for i in pairs :
        if (i.split("-")[1] == volunteer_email) :
            l = i.split("-")
            l.append(pairs[i]["status"])
            row.append(l)
    return HttpResponse(json.dumps(row), content_type='application/json') 