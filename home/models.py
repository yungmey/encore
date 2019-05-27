# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class TUser(models.Model):
    # id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    email = models.CharField(max_length=20, blank=True, null=True)
    salt = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=70, blank=True, null=True)
    c_time = models.DateTimeField(auto_now_add=True)
    has_confirm =models.BooleanField(default=False,verbose_name='是否确认')

    class Meta:
        # managed = False
        db_table = 't_user'

class Confirm_string(models.Model):
    code = models.CharField(max_length=256,verbose_name='用户注册码')
    user = models.ForeignKey('TUser',on_delete=models.CASCADE,verbose_name='关联的用户')
    code_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        # managed = False
        db_table = 't_confirm'


class TGoods(models.Model):
    bookname = models.CharField(max_length=20, blank=True, null=True)
    artist = models.CharField(max_length=10, blank=True, null=True)
    classid = models.ForeignKey('TClass', models.DO_NOTHING, db_column='classid', blank=True, null=True)
    marketprice = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    sales = models.BigIntegerField(blank=True, null=True)
    comments = models.BigIntegerField(blank=True, null=True)
    markettime = models.DateField(blank=True, null=True)
    picture = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 't_goods'


class TClass(models.Model):
    classname = models.CharField(max_length=20, blank=True, null=True)
    parent_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 't_class'


class TOrder(models.Model):
    order_price = models.FloatField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=40, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    receive_address = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 't_order'

class TOrderitem(models.Model):
    book_name = models.CharField(max_length=40, blank=True, null=True)
    sub_total = models.FloatField(blank=True, null=True)
    order = models.ForeignKey(TOrder, models.DO_NOTHING, blank=True, null=True)
    book = models.ForeignKey(TGoods, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 't_orderitem'


class TAddress(models.Model):
    username = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=30, blank=True,null=True)
    usercode = models.IntegerField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    sellphone = models.IntegerField(blank=True, null=True)
    info = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    listnote = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 't_address'