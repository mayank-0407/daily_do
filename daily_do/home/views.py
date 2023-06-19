from datetime import date,datetime,timedelta
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import math
import random
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.
def temp(request):
    return render(request,'home/send_task.html')

def SENDMAIL(subject, message, email):
    print('insideeee send imailwa')
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    try:
        checker = User.objects.get(email=email)
    except:
        print('nhi mili bhai email')
    username = checker.first_name
    html_content = render_to_string("home/main_email.html",{'message': message, 'user_name': username})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject,text_content,email_from,recipient_list)
    email.mixed_subtype = 'related'
    email.attach_alternative(html_content,"text/html")
    email.send()

def SENDTASK(subject, message, email):
    print('insideeee send imailwa')
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    try:
        checker = User.objects.get(email=email)
    except:
        print('nhi mili bhai email')
    username = checker.first_name
    html_content = render_to_string("home/send_task.html",{'message': message, 'user_name': username})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject,text_content,email_from,recipient_list)
    email.mixed_subtype = 'related'
    email.attach_alternative(html_content,"text/html")
    email.send()
    
def generate_code(length):
    digits = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code = ""
    for i in range(length) :
        code += digits[math.floor(random.random() * 62)]
    return code

def send_activate_email(user,email):
    myuser=User.objects.get(email=user.email)
    print(myuser)
    if not myuser.is_active:
        try:
            myotp=myuser.username + generate_code(60)
            try:
                OTP.objects.create(user=myuser,otp_code=myotp)
            except:
                print('huh')
            print(myotp)
            url=settings.BASE_URL_EMAIL+'/signup/verify/'+myotp
            email_subject='Account Verification Request In Daily-TODO'
            email_message='You need To veriy you email in order to continue to our website\n'+'Activation Link:- '+ url
            SENDMAIL(email_subject,email_message,email)
            return True
        except:
            return False

def send_task_email(user,email):
    try:
        try:
            myuser=User.objects.get(email=user.email)
            print(myuser)
            mymessage=Works.objects.filter(user=myuser)
        except:
            print('messagewa nhi mila')
        email_subject='Task List From Daily_do'
        SENDTASK(email_subject,mymessage,email)
        return True
    except:
        return False
        
def send_task_trigger(request):
    user=User.objects.get(email=request.user.email)
    email=request.user.email
    if send_task_email(user,email):
        messages.success(request,'Email Sent Successfully')
        return redirect('dashboard')
    else:
        messages.error(request,'Email Not Sent')
        return redirect('dashboard')
        
def signin(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        temp_email=request.POST.get('email')
        password=request.POST.get('pass1')
        
        email=temp_email.lower()
            
        # resend code
        try:
            verify_user=User.objects.get(username=email)    
        except:
            try:
                verify_user=User.objects.get(email=email)    
            except:
                print('login wala errorwa')
                messages.error(request, 'Error - No User found!')
                return redirect('signup')  
        if verify_user.is_active == False:
            try:
                if send_activate_email(verify_user,verify_user.email):
                    messages.error(request, 'Your Email is not yet verified. So we have Sent Link to your email ,verify that to continue')
                    return redirect('signup')  
                else:
                    messages.error(request, 'Your Email is not yet verified, Unable to send link')
                    return redirect('signup')  
            except:
                print('Unable to send email')
        try:
            tempuser=User.objects.get(email=email).username                  
            user=authenticate(request,username=tempuser,password=password)
        except:
            try:
                User.objects.get(username=email)
                
                user=authenticate(request,username=email,password=password)
                
            except:    
                messages.error(request, 'Error - Entered Username or Email is Not in our records.')
                return redirect('signup')
                  
        if user == None: 
            messages.error(request, 'Error - No User Exists.')
            return redirect('signup')
        
        if user.is_active:
            login(request,user)
            return redirect('dashboard')
        
        else:
            messages.error(request, 'Error - You dont have permission to login.')
            return redirect('signup')
        
    else:
        return render(request,"home/login.html")

def signout(request):
    logout(request)
    return redirect('signin')

def dashboard(request):
    try:
        myuser = User.objects.get(email=request.user.email)
    except:
        print('nhi mili bhai email')
    work=Works.objects.filter(user=myuser,is_active=True)
    return render(request,"home/dashboard.html",context={"work":work})


def add_work(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            main_text = request.POST.get('main_text')
            temp_s_date = request.POST.get('date')
            temp_today = date.today()
            s_date=datetime.strptime(str(temp_s_date),'%Y-%m-%d').date()
            today=datetime.strptime(str(temp_today),'%Y-%m-%d').date()  
            # print(s_date)
            try:
                myuser = User.objects.get(email=request.user.email)
            except:
                print('nhi mili bhai email')
            # print(myuser.email)
            try:
                my_object=Works.objects.create(user=myuser,todo=str(main_text),start_date=today,end_date=s_date)
                messages.error(request, 'Work was Added successfully')
                return redirect('dashboard')
            except:
                messages.error(request, 'Work was Not Added successfully')
                return redirect('dashboard')

        return redirect('dashboard')
    return redirect('dashboard')

def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
            # temp_username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            temp_email = request.POST.get('email')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')

            email=temp_email.lower()
            username=email
            
            if not pass1==pass2:
                messages.error(request, 'Error - Entered Passwords are same.')
                return redirect('signup')

            try:
                User.objects.get(email=email)
                messages.error(request, 'Error - Email Already exists.')
                return redirect('signup')
            except:
                pass
        
            myuser=User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name)
            myuser.is_active=False
            myuser.set_password(pass1)
            myuser.save()
            
            if send_activate_email(myuser,email):
                messages.error(request, 'Success - Verification link has been sent to your email. So Check You email and verify You email within 3 min otherwise link will expire')
                return redirect('signup')
            else:
                messages.error(request, 'Error - Unable to send Notification. But your Account has been created but you will not be able to login as it is inactive so signin to resend link')
                return redirect('signup')

    return render(request, 'home/signup.html')

def activate_by_email(request,code):
    if True:
        myotp = OTP.objects.get(otp_code=code)
        print(myotp)  
    # except:
    #     print('No User Found')
    if myotp.user.is_active:
        return render(request,'home/email.html')
    myuser=myotp.user
    myuser.is_active=True
    myuser.save()
    email=myuser.email
    try:
        email_message='Account Verified In Daily-TODO'
        email_subject='Your Account at Daily-TODO has been created Verified Visit our page to avail amazing experience'
        SENDMAIL(email_message,email_subject,email)
    except Exception as e:
        print("Can't send email\n", str(e))

    return render(request,'home/email.html')

def del_work(request,id):
    if request.user.is_authenticated:
        try:
            work = Works.objects.get(id = int(id))
            work.delete()
            messages.error(request, 'Success - Work Deleted Successfully')
            return redirect('dashboard')
        except:
            messages.error(request, 'Error - While Fetching the Work')
            return redirect('dashboard')
    return redirect('signup')

def apply_filter(request):
    if request.user.is_authenticated:
        try:
            myuser = User.objects.get(email=request.user.email)
        except:
            print('nhi mili bhai email')
        work=Works.objects.filter(user=myuser)
        return render(request,"home/dashboard.html",context={"work":work})
    return redirect('signup')
