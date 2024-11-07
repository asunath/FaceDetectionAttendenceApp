from django.urls import path
from User import views


urlpatterns = [

    # LINK TO PROFILE PAGE
    path('profile/', views.profile, name="profile"),

    # DISPLAY ALL THE LEAVE REQUESTS
    path('requestleave/', views.leaverequests, name="requestleave"),

    # SHOW LEAVE HISTORY
    path('reqhistory/', views.reqhistory, name="reqhistory"),

    path('changepassword/', views.changePassword, name="changepassword"),

    path('attendance/', views.attendance, name="attendance"),
]