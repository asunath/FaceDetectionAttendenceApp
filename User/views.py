from django.shortcuts import redirect, render
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from Admin.models import leaveRequests
from Facerecognition.models import Attendance
from User.models import userLeave, userprofile

# Create your views here.



@login_required(login_url='loginpage')
def profile(request):
    if request.user.is_authenticated:
        user_profile = userprofile.objects.get(user=request.user)
        return render(request, 'User/profile.html', {'user_profile': user_profile})
    else:
        return redirect('loginpage')
    


@login_required(login_url='loginpage')
def leaverequests(request):
    leave_available = userLeave.objects.filter(user=request.user)
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
    if request.method == 'POST':
        name = userprofile.objects.filter(user=request.user).values('name')
        leave_type = request.POST.get('leavetype')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')
        reason = request.POST.get('reason')

        new_request = leaveRequests(user = request.user, name = name, type=leave_type, startDate=start_date, endDate=end_date, reason=reason)
        new_request.save()

        return redirect("requestleave")

    return render(request, "User/leave.html", {'leave_available': list(leave_data)})



@login_required(login_url='loginpage')
def reqhistory(request):
    requests = leaveRequests.objects.filter(user=request.user)
    requests = reversed(requests)
    return render(request, "User/reqhistory.html", {"requests":requests})



def changePassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('oldPassword')
        new_password = request.POST.get('newPassword')
        
        # Check if old password is correct
        if request.user.check_password(old_password):
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Update session to prevent auto logout
            message = "Password changed successfully"
            return render(request, "User/changepassword.html", {'message': message})
        else:
            message = "Incorrect Old password"
            return render(request, "User/changepassword.html", {'message': message})
    else:
        message = ""
        return render(request, "User/changepassword.html", {'message': message})



def attendance(request):
    attendance_data = list(Attendance.objects.filter(user = request.user).values('timestamp'))
    for record in attendance_data:
        record['timestamp'] = record['timestamp'].isoformat()
    return render(request, "User/attendance.html", {'attendance_data': attendance_data})