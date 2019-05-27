from django.contrib import admin
from django.urls import path
from home import views

app_name='home'
urlpatterns=[
    path('admin/', admin.site.urls),
    path('booklist/', views.booklist,name='booklist'),
    path('homepage/',views.homepage,name='homepage'),
    path('detail/',views.detail,name='detail'),
    path('login/',views.login,name='login'),
    path('loginlogic/',views.loginlogic,name='loginlogic'),
    path('loginout/',views.loginout,name='loginout'),
    path('regist/',views.regist,name='regist'),
    path('registlogic/',views.registlogic,name='registlogic'),
    path('getcaptcha/',views.getcaptcha,name='getcaptcha'),
    path('checkname/',views.checkname,name='checkname'),
    path('emailcheck/',views.emailcheck,name='emailcheck'),
    path('car/',views.car,name='car'),
    path('addcar/',views.addcar,name='addcar'),
    path('upcar/',views.upcar,name='upcar'),
    path('car_remove/',views.car_remove,name='car_remove'),
    path('indent/',views.indent,name='indent'),
    path('indent_ok/',views.indent_ok,name='indent_ok'),

]
