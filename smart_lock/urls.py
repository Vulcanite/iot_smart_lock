from django.urls import path

from . import views
from . import views1

urlpatterns = [
    path('restricted', views.restricted, name='restricted'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('chatbot', views.chatbot, name='chatbot'),
    path('logs', views.table_data, name='logs'),
    path('', views.loginPage, name='login'),
    path('form', views.registerPage, name='form'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('rec_feed', views.recognizer_feed, name='rec_feed'),
    path('logout', views.logoutUser, name="logout"),
    path('send_otp', views.send_otp, name="send_otp"),
    path('verify_otp', views.verify_otp, name="verify_otp"),
    path('chat', views.chat_text, name="chat"),
    path('get', views1.chatbot, name="get")
]
