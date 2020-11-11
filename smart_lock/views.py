import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from django.http.response import StreamingHttpResponse
from django.shortcuts import render, redirect
from smart_lock.camera import VideoCamera, IPWebCam
from smart_lock.decorators import unauthenticated_user, allowed_users, admin_only
from smart_lock.models import logs
from datetime import date
from django.http import JsonResponse


@login_required(login_url='login')
def restricted(request):
    return render(request, "restricted.html")


@login_required(login_url='login')
def dashboard(request):
    log = logs.objects.filter(VISIT_TIME__date=date.today()).order_by('-VISIT_TIME')[:5]
    return render(request, "dashboard.html", {'log': log})


@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN', 'VIEW_UNLOCK'])
def unlock(request):
    return render(request, "unlock.html")


@login_required(login_url='login')
def chatbot(request):
    return render(request, "chatbot.html")


# CAMERA SETUP
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def webcam_feed(request):
    return StreamingHttpResponse(gen(IPWebCam()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


# REGISTRATION
@login_required(login_url='login')
@admin_only
def registerPage(request):
    if request.method == 'POST':
        user_reg = User(first_name=request.POST.get('first_name'),
                        password=request.POST.get('password1'),
                        username=request.POST.get('username'))
        try:
            user_reg.save()
            groups = Group.objects.get(name=request.POST.get('access_level'))
            groups.user_set.add(user_reg)
            context = {'folder_name': request.POST.get('first_name')}
            return render(request, "dataset.html", context)
        except IntegrityError:
            messages.info(request, "Username already present!!")
    return render(request, 'form.html')


# LOGIN
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'login.html')


# LOGOUT
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


# SEND OTP
@login_required(login_url='login')
def send_otp(request):
    url = "http://2factor.in/API/V1/c220d523-1bb4-11eb-b380-0200cd936042/SMS/9769788150/AUTOGEN"
    payload = ""
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.request("GET", url, data=payload, headers=headers)
    data = response.json()
    request.session['otp_session_data'] = data['Details']
    print(data['Details'])
    return JsonResponse({'data':data})


# VERIFY OTP
@login_required(login_url='login')
def verify_otp(request):
    user_otp = request.POST.get('votp')
    print(user_otp)
    session_id= request.session['otp_session_data']
    print(session_key)
    url = "http://2factor.in/API/V1/c220d523-1bb4-11eb-b380-0200cd936042/SMS/VERIFY/"+session_id+"/"+str(user_otp)
    print(url)
    payload = ""
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.request("GET", url)
    data = response.json()
    if data['Status'] == "Success":
        return redirect('dashboard')
    return render(request, "dashboard.html")


# TABLE DATA
@login_required(login_url='login')
@admin_only
def table_data(request):
    records = logs.objects.all().order_by('-VISIT_TIME')
    count = logs.objects.count()
    return render(request, 'logs.html', {'records': records, 'count': count})



#, data=payload, headers=headers