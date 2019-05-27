from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
import os,uuid,json,random,hashlib

from home.captcha.image import ImageCaptcha
import random,string
from django.core.paginator import Paginator
from datetime import datetime
# Create your views here.

from home.models import TGoods,TUser,TClass,TOrderitem,TOrder,TAddress,Confirm_string
from home.cart import Cartitem,Addcar

#注册页面
def regist(request):
    name =request.session.get('emailname')
    if name:
        return render(request,'home/homepage.html',{'name':name})
    return render(request, 'home/regist.html')


#注册验证
def registlogic(request):
    email = request.POST.get('username')
    pwd= request.POST.get('password')

    def get_salt():
        l = '1234567890-=qwertyuiop[]asdfghjklzxcvbnm,./'
        salt=''.join(random.sample(l,6))
        return salt

    salt=get_salt()
    pwdd=pwd+salt
    #密码+加盐产生的6位数字符串

    h = hashlib.md5()
    h.update(pwdd.encode())
    # 生成2进制密码
    # pwd=h.digest()
    # 生成16进制密码
    password = h.hexdigest()
    #把加盐和密码组合产生的字符串进行md5加密

    session_code = request.session["code"]
    cap_code = request.POST["int_captcha"]
    print(session_code, cap_code)

    if session_code.lower() == cap_code.lower():
        new_user = TUser.objects.create(email=email,salt=salt,password=password)
        code = make_confirm_string(new_user)
        request.session['emailcode'] = code
        send_email(email, code)   #邮箱发送邮件
        return render(request,"home/registok.html",{'email':email})
    return redirect('home:login')


# 注册邮箱验证
def emailcheck(request):
    email = request.GET.get('email')
    print(email)

    int_cap=request.POST.get('int_cap')
    sendemailcode =request.session.get('emailcode')

    print(int_cap,sendemailcode)
    if int_cap == sendemailcode:
        confirm = TUser.objects.filter(email=email)[0]
        confirm.has_confirm = 1
        confirm.save()
        return render(request,'home/login.html')
    return HttpResponse('邮箱验证失败')


#注册邮箱md5加密
def hash_code(name, now):
    h = hashlib.md5()
    name += now
    h.update(name.encode())
    return h.hexdigest()

#邮箱验证码数据处理
def make_confirm_string(new_user):
    now = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    code = hash_code(new_user.email, now)
    Confirm_string.objects.create(code=code,user=new_user)
    return code

#发送邮件
def send_email(email, code):
    subject = 'python157'
    from_email = 'yungmey@sina.com'
    # subject, from_email, to ='python157','huichom@163.com', 'yungmey@163.com'
    text_content = '欢迎访问www.baidu.com，祝贺你收到我的邮件，有幸收到我的邮件说明你及其幸运'
    html_content = '<p>感谢注册<a href="http://{}/confirm/?code={}"target = blank > www.baidu.com < / a >, \欢迎你来验证你的邮箱，验证结束你就可以登陆了！< / p > '.format('127.0.0.1', code)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content,"text/html")
    msg.send()


#登陆和注册邮箱是否已注册判断
def checkname(request):
    username = request.GET.get('username')
    print('name=',username)
    users=TUser.objects.filter(email=username)
    print(users)
    if users:
        return HttpResponse('用户名是已注册账号')
    return HttpResponse('用户名没有被注册')

#验证码生成
def getcaptcha(request):
    image = ImageCaptcha()
    code = random.sample(string.ascii_letters+string.digits,2)
    random_code ="".join(code)
    request.session['code']=random_code
    data = image.generate(code)
    print(data)
    return HttpResponse(data,"image/png")


#登陆页面
def login(request):
    username = request.COOKIES.get('name')
    password = request.COOKIES.get('password')

    returnurl =request.GET.get('returnurl')
    print(returnurl,'ooooo')
    name =request.session.get('emailname')
    result = TUser.objects.filter(email=username, password=password)

    #如果cookie和session正确直接登录
    if result and name:
        return redirect('home:homepage')

    else:
        return render(request,'home/login.html')


#登陆验证
def loginlogic(request):
    name = request.POST.get('username')
    pwd = request.POST.get('pwd')
    cap_code = request.POST.get('int_cap')


    #查看登录账号是否经过邮箱验证，没验证不允许登陆
    confirm= TUser.objects.filter(email=name)[0].has_confirm

    salt=TUser.objects.get(email=name).salt
    pwdd=pwd+salt
    print(salt)
    #获取输入的密码+数据库中的盐

    h = hashlib.md5()
    h.update(pwdd.encode())
    # 生成2进制密码
    # pwd=h.digest()
    # 生成16进制密码
    password = h.hexdigest()
    #把加盐和密码组合产生的字符串进行md5加密

    uber=TUser.objects.filter(email=name,password=password)
    print(name,password)

    session_code = request.session["code"]

    print(session_code, cap_code)

    print(uber)

    if uber and session_code.lower() == cap_code.lower() and confirm == 1:
        rem = request.POST.get('autologin')
        #登陆后创建一个session，值为注册的邮箱
        request.session['emailname'] = name
        res = redirect('home:homepage')

        if rem:
            res.set_cookie('name',name,max_age=0)
            res.set_cookie('password',password, max_age=0)
        return res
    return render(request,'home/login.html')


#登出
def loginout(request):
    #获取点击退出的原页面路径
    returnur =request.GET.get('returnurl')
    #删除登录创建的session
    del request.session['emailname']

    if returnur == car:
        return redirect('home:car')
    return redirect('home:homepage')


#当当首页
def homepage(request):
    res = TClass.objects.filter(parent_id=0)
    res1 = TClass.objects.filter(parent_id__gt=0)

    #获取登录状态
    name = request.session.get('emailname')

    #分页
    number = request.GET.get('page')
    users = TGoods.objects.all()
    pagtor = Paginator(users,per_page=8)
    if number is None:
        number = 1
    page = pagtor.page(number)

    uc=TGoods.objects.all().order_by('-comments')
    pagtor2 = Paginator(uc, per_page=8)
    if number is None:
        number = 1
    page2 = pagtor2.page(number)

    ud = TGoods.objects.all().order_by('-sales')
    pagtor3 = Paginator(ud, per_page=8)
    if number is None:
        number = 1
    page3 = pagtor3.page(number)

    if name:
        return render(request, 'home/homepage.html',{'res':res,'res1':res1,'page':page,'psc':page2,'psd':page3,'name':name})
    return render(request, 'home/homepage.html',{'res': res, 'res1': res1, 'page': page, 'psc': page2, 'psd': page3})

#当当分类页
def booklist(request):
    res = TClass.objects.filter(parent_id=0)
    res1 = TClass.objects.filter(parent_id__gt=0)

    name = request.session.get('emailname')
    classname =request.GET.get('name1')
    bookid=TClass.objects.get(classname=classname).pk
    bookinf=TGoods.objects.filter(classid=bookid)
    print(bookinf)
    return render(request,'home/booklist.html',{'res':res,'res1':res1,'classname':classname,'book':bookinf,'name':name})


#当当详情页
def detail(request):
    bookname = request.GET.get('bookname')
    book = TGoods.objects.get(bookname=bookname)

    bookclassid = TGoods.objects.get(bookname=bookname).classid
    print(bookclassid)

    # bookclass = TClass.objects.get(pk=bookclassid).pk
    # bookinf = TClass.objects.get(pk=bookclassid).classname
    # bookclass1=TClass.objects.get(pk=bookinf)

    name = request.session.get('emailname')
    print(book)
    # print(bookclass)
    # print(bookclass1)
    return render(request,'home/detail.html',{'book':book,'name':name})


#当当购物车页面
def car(request):
    name= request.session.get('emailname')
    cart= request.session.get('cart')
    return render(request,'home/car.html',{'cart':cart,'name':name})


#增加书籍
def addcar(request):
    bookid =request.GET.get('bookid')
    print(bookid)
    book = TGoods.objects.filter(id=bookid)[0]

    cart = request.session.get('cart')
    if not cart:
        cart = Addcar()

    cartitem = Cartitem(book, 1)
    cart.add(cartitem)
    request.session['cart'] =cart

    print(cart)
    return HttpResponse('ok')


# 购物车页更改书籍数目
def upcar(request):
    cid = request.GET.get('item_id')
    new_amount = int(request.GET.get('new_amount'))
    cart = request.session.get('cart')

    print(cid,new_amount)
    cart.upc(cid,new_amount)

    request.session['cart'] = cart
    s1 = cart.upc(cid,new_amount)
    s2 = cart.totalprice
    s3 = cart.amount
    s4 = cart.save
    js = {'s1':s1,'s2':s2,'s3':s3,'s4':s4}
    return JsonResponse(js)

# 购物车删除书籍
def car_remove(request):
    info_id = request.GET.get('info_id')
    cart = request.session.get('cart')
    cart.remove(info_id)
    request.session['cart'] = cart
    s2 = cart.totalprice
    s3 = cart.amount
    s4 = cart.save
    js = {'s2': s2, 's3': s3, 's4': s4}
    return JsonResponse(js)


#填写邮寄地址
def indent(request):
    del request.session['cart']
    name =request.session.get('emailname')
    #判断是否是登录状态
    if name:
        return render(request,'home/indent.html',{'name':name})
    return redirect('home:login')

# 邮寄地址确认
def indent_ok(request):
    name = request.session.get('emailname')
    # 判断是否是登录状态
    if name:
        username =request.POST.get('username')
        country =request.POST.get('country_id')
        province =request.POST.get('province_id')
        city =request.POST.get('city_id')
        town =request.POST.get('town_id')
        quarter =request.POST.get('quarter_id')
        address1 =request.POST.get('ship_man')

        address=country+province+city+town+quarter+address1
        emailcode=request.POST.get('ship_code')
        sellphone=request.POST.get('ship_sellphone')
        phone=request.POST.get('ship_phone')
        TAddress.objects.create(username=username, address=address, usercode=emailcode, sellphone=sellphone, phone=phone)
        return render(request,'home/indent_ok.html',{'name':name})
    return render(request, 'home/homepage.html')


