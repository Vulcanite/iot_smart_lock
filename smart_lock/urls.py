from django.urls import path

from . import views
from . import views1

urlpatterns = [
    path('restricted', views.restricted, name='restricted'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('chatbot', views.chatbot, name='chatbot'),
    path('unlock', views.unlock, name='unlock'),
    path('logs', views.table_data, name='logs'),
    path('', views.loginPage, name='login'),
    path('form', views.registerPage, name='form'),
    path('webcam_feed', views.webcam_feed, name='webcam_feed'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('logout', views.logoutUser, name="logout"),
    path('send_otp', views.send_otp, name="send_otp"),
    path('verify_otp', views.verify_otp, name="verify_otp"),
    path('bot_response', views1.chatbot, name="bot_response")
]
