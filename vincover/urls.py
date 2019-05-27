from django.urls import path
from vincover import views


app_name='vincover'
urlpatterns=[
    path('regist/',views.regist,name='regist'),
    path('registlogic/',views.registlogic,name='registlogic'),
    path('checkname/',views.checkname,name='checkname'),
    path('checkpwd/',views.checkpwd,name='checkpwd'),
    path('checkconfirmpwd/',views.checkconfirmpwd,name='checkconfirmpwd'),

]