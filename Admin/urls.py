from django.urls import path
from Admin import views


urlpatterns = [

    # LINK TO HOME PAGE
    path('', views.home, name="home"),


    # LINK TO LOGIN PAGE
    path('loginpage/', views.loginpage, name="loginpage"),


    # LINK TO REGISTER PAGE
    path('registration/', views.registration, name="registration"),


    # LOGOUT FUNCTION
    path('logout/', views.logoutUser, name="logout"),


    # REQUEST FOR LEAVE
    path('requestlist/', views.requestlist, name="requestlist"),

    # APPROVE THE LEAVE REQUEST
    path('approve/<int:req>', views.approve, name="approve"),


    # REJECT THE LEAVE REQUEST
    path('reject/<int:reqid>', views.reject, name="reject"),


    # LOAD ADMIN DASHBOARD
    path('admindash/', views.admindashboard, name="admindash"),


    # TO SHOW ALL USERS BY ADMIN
    path('users/', views.listusers, name="users"),

    # LINK TO DELETE A USER
    path('deleteuser/<int:reqid>', views.deleteuser, name="deleteuser"),


    path('api/userLeaveHistory/<int:user_id>/', views.userLeaveHistory, name="userLeaveHistory"),


    path('manageleavetypes/', views.manageleavetypes, name="manageleavetypes"),


    path('manageleavetypes/update-leave-limit/', views.resetLimit, name="update-leave-limit"),


    path('manageleavetypes/api/resetLeaveAvailable/', views.resetLeaveAvailable, name="resetLeaveAvailable"),
]