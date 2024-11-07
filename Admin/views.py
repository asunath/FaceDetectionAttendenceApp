from datetime import date
from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from Admin.models import *
from User.models import *
from Facerecognition.models import *

# Create your views here.



def home(request):
    return render(request, "home.html")



def loginpage(request):
    message = ""
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=email)
        except:
            message = "User does not exist"
            return render(request, "Admin/loginpage.html", {'message': message})


        user = authenticate(request, username=email,password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admindash')
            else:
                return redirect('profile')
        else:
            message = "Invalid Password"
            return render(request, "Admin/loginpage.html", {'message': message})
    
    return render(request, "Admin/loginpage.html", {'message': message})



def logoutUser(request):
    logout(request)
    return redirect('loginpage')



# registration form
@login_required(login_url='loginpage')
def registration(request):
    if request.method == "POST":
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        doj = request.POST.get('doj')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        address = request.POST.get('address')

        image = request.FILES.get('image')


        date = datetime.strptime(dob, '%Y-%m-%d')
        password = date.strftime('%d%m%Y')

        # newuser = User(username=email,name=name,email=email,password=password)
        try:
            newuser = User.objects.create_user(
                username=email,email=email,password=password)
            newuser.save()
        except IntegrityError:
            return render(request, "Admin/registration.html", {'user_exists' : True})

        profile = userprofile.objects.create(
            user = newuser, 
            name = name, 
            gender = gender, 
            dob = dob, 
            mobile = mobile, 
            email = email, 
            doj = doj, 
            city = city, 
            state = state, 
            country = country, 
            address = address,
            image = image
        )
        profile.save()

        leave_types = leaveType.objects.all()
        for leave_type in leave_types:
            user_leave_entry = userLeave.objects.create(
                user = newuser,
                leave_type = leave_type,
                remaining_leaves = leave_type.limit
            )
            user_leave_entry.save()

        # send email message
        registration_completion_email(profile.name,profile.email)

        return render(request, "Admin/registration.html")
    return render(request, "Admin/registration.html")



def manageleavetypes(request):
    leave_types = leaveType.objects.all()

    if request.method == 'POST':
        form = request.POST.get('form_type')
        if form == 'limit_change_form':
            for leave_type in leave_types:
                new_limit = request.POST.get(leave_type.name)
                if new_limit is not None:
                    leave_type.limit = int(new_limit)
                    leave_type.save()
        
        # Handle other form submissions here

        if form == 'add_new_form':
            leaveName = request.POST.get('type_name')
            leaveLimit = request.POST.get('limit')
            new_leave_type = leaveType(name = leaveName, limit = leaveLimit)
            new_leave_type.save()
            users = User.objects.all()
            for user in users:
                user_leave_entry = userLeave.objects.create(
                    user = user,
                    leave_type = new_leave_type,
                    remaining_leaves = new_leave_type.limit
                )
                user_leave_entry.save()

    return render(request, "Admin/leavetypes.html",{'leave_types': leave_types})



@login_required(login_url='loginpage')
def requestlist(request):
    requests = leaveRequests.objects.filter(status="Submitted")
    requests = reversed(requests)
    return render(request, "Admin/requestlist.html", {"requests":requests})



@login_required(login_url='loginpage')
def approve(request, req):
    req = leaveRequests.objects.get(id=req)
    req.status="Approved"
    req.save()
    leave_available = userLeave.objects.get(user=req.user, leave_type__name = req.type)

    # TO REDUCE NUMBER OF CASUAL LEAVES ALLOWED
    difference = date_distance(req.startDate,req.endDate)
    leave_available.remaining_leaves -= difference.days
    leave_available.save()
    
    user = req.user
    subject = 'Leave request approval'
    message = f'Your leave request for {req.startDate} to {req.endDate} has been approved.'
    email_notification(subject, message, req.name, user.email)
        
    return redirect("requestlist")



# FUNCTION FOR REQUEST REJECTION
@login_required(login_url='loginpage')
def reject(request,reqid):
    req = leaveRequests.objects.get(id=reqid)
    req.status = "Rejected"
    req.save()
    user = req.user
    subject = 'Leave request rejected'
    message = f'Your leave request for {req.startDate} to {req.endDate} has been rejected.'
    email_notification(subject, message, req.name, user.email)
    return redirect("requestlist")



# ADMIN DASHBOARD
@login_required(login_url='loginpage')
def admindashboard(request):
    pending = leaveRequests.objects.filter(status="Submitted").count()
    user_count = User.objects.filter(is_staff=False, is_superuser=False).count()
    on_leave = on_leave_today()
    present_today = attendance_today()
    return render(request, "Admin/admindash.html",{"pending":pending, "user_count":user_count, "on_leave":on_leave, "present":present_today})



# TO DISPLAY ALL THE REGISTERED USERS
@login_required(login_url='loginpage')
def listusers(request):
    all_users = User.objects.filter(is_superuser = False)
    user_profile = []
    for user in all_users:
        profile = user.userprofile
        user_details = {
            'id': user.id,
            'name': profile.name,
            'email': profile.email
        }
        user_profile.append(user_details)
    return render(request, "Admin/listusers.html",{"all_users":user_profile})



# TO DELETE A USER
@login_required(login_url='loginpage')
def deleteuser(request,reqid):
    user = User.objects.get(id=reqid)
    user.delete()
    return redirect("users")



# FOR ADMIN TO VIEW INDIVIDUAL USER'S LEAVE HISTORY
def userLeaveHistory(request, user_id):
    user_history = leaveRequests.objects.filter(user_id=user_id).values()
    leave_available = userLeave.objects.filter(user_id=user_id)
    leave_data = []
    for leave in leave_available:
        leave_type = leave.leave_type.name
        remaining_leave = leave.remaining_leaves
        limit = leave.leave_type.limit
        leave_data.append({
            'limit': limit,
            'leave_type': leave_type,
            'remaining': remaining_leave
        })

    data = {
        'user_history': list(user_history),
        'leave_available': list(leave_data),
    }
    return JsonResponse(data)



def resetLimit(request):

    if request.method == 'POST':
        leave_type_id = request.POST.get('leave_type_id')
        new_limit = request.POST.get('new_limit')

        # Update leave limit in the database
        leave_type = leaveType.objects.get(id=leave_type_id)
        leave_type.limit = new_limit
        leave_type.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'}, status=400)



def resetLeaveAvailable(request):
    # Get all leave types
    leave_types = leaveType.objects.all()

    # Iterate through each leave type
    for leave_type in leave_types:
        # Get the limit for the leave type
        limit = leave_type.limit

        # Update remaining leaves for all users with this leave type
        user_leaves = userLeave.objects.filter(leave_type=leave_type)
        for user_leave in user_leaves:
            user_leave.remaining_leaves = limit
            user_leave.save()
    return JsonResponse({'status': 'Leave Available Changed Successfully'})










def attendance_today():
    today = date.today()
    return Attendance.objects.filter(timestamp__date=today).count()


def on_leave_today():
    today = date.today()
    return leaveRequests.objects.filter(startDate__lte=today, endDate__gte=today, status="Approved").count()


def date_distance(fromDate,toDate):
    return abs(toDate-fromDate)


def registration_completion_email(name,email):
    subject = 'Welcome to Our Leave Management System!'
    message = f"""Dear {name},

We are pleased to inform you that you have been successfully registered for our Leave Management System. This system will facilitate the management of your leaves and ensure smoother coordination within our organization.

Your login credentials are as follows:

Username: {email}
Password: Your birthday date in the format DDMMYYYY
For example, if your birthday is April 8th, 1990, your password would be 08041990.

Please log in at [Leave Management System URL] using the provided credentials. Once logged in, you will be able to submit leave requests, view your leave balances, and track the status of your requests.

If you encounter any difficulties logging in or have any questions regarding the system, please don't hesitate to contact our support team at [support email or contact number].

Thank you for being a part of our Leave Management System. We trust that this tool will enhance your leave management experience and contribute to greater efficiency across the organization.

Best regards,
System Administrator
The Insightful Eye"""
    
    email_from = settings.EMAIL_HOST_USER
    # recipient_list = [user.email, ]
    recipient = [email,]
    send_mail( subject, message, email_from, recipient )
    return redirect('registration')



def email_notification(subject, message, name, email):
    subject = subject
    message = message
    email_from = settings.EMAIL_HOST_USER
    recipient = [email,]
    send_mail( subject, message, email_from, recipient )



