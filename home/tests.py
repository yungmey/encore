from datetime import datetime
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "encore.settings")
django.setup()

import random,hashlib
from home.models import TGoods,TUser

# good =TGoods.objects.get(pk='8')
# good.picture='pics/p333.jpg'
# good.save()

# pwd='123456'
# def get_salt():
#     l='1234567890-=qwertyuiop[]asdfghjklzxcvbnm,./'
#     salt=''.join(random.sample(l,6))
#     return salt
#
# salt=get_salt()
# pwdd=pwd+salt
#
# #创建哈希对象
# h=hashlib.md5()
# #加载密码
# h.update(pwdd.encode())
# #生成2进制密码
# #pwd=h.digest()
# #生成16进制密码
#
# pwddd=h.hexdigest()
# print(pwd)
# print(pwdd)
# print(pwddd)


# teo=TUser.objects.get(email='123@163.com').salt
# print(teo)

# def getsession(req):
#     print(req.session['bookname'])



# now = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
# print(now)