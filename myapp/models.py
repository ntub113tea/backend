# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.db import transaction

class CustomerManager(BaseUserManager):
    def create_user(self, customer_id, password=None, **extra_fields):
        if not customer_id:
            raise ValueError('The Customer ID must be set')
        
        user = self.model(customer_id=customer_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, customer_id, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(customer_id=customer_id, password=password, **extra_fields)
    def has_module_perms(self, app_label):
        # 在这里实现 has_module_perms 方法逻辑
        return True
    
class DailyCounter(models.Model):
    date = models.DateField(default=timezone.now)
    counter = models.IntegerField(default=0)

    class Meta:
        db_table = 'dailycounter'
        
    @classmethod
    @transaction.atomic
    def get_next_counter(cls):
        today = timezone.now().date()
        counter_obj, created = cls.objects.select_for_update().get_or_create(date=today)
        next_counter = counter_obj.counter + 1
        counter_obj.counter = next_counter
        counter_obj.save()
        return next_counter

class Customer(AbstractBaseUser,PermissionsMixin):
    GENDER_CHOICES = (
        ('男', '男'),
        ('女', '女'),
    )
    customer_id = models.CharField(primary_key=True,max_length=15,verbose_name="user_id")
    password = models.CharField(max_length=128)
    customer_name = models.CharField(max_length=10,verbose_name="name")
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.IntegerField()
    line_id = models.CharField(max_length=45, blank=True, null=True)
    last_login = models.DateTimeField('last login', default=timezone.now, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomerManager()

    USERNAME_FIELD = 'customer_id'
    REQUIRED_FIELDS = ['customer_name', 'sex', 'age']  #  password 不能列在這
    def __str__(self):
        return f"{self.customer_name} ({self.customer_id})"
    class Meta:
        managed = False
        db_table = 'customer'
        verbose_name = 'User'


class HerbStock(models.Model):
    herbs_id = models.IntegerField(primary_key=True)
    herbs_name = models.CharField(max_length=10)
    current_stock = models.FloatField()

    class Meta:
        managed = False
        db_table = 'herb_stock'


class Purchase(models.Model):
    purchases_id = models.IntegerField(primary_key=True,editable=False) #editable此值不可改動 因為有自動+1
    herbs_id = models.IntegerField()
    supply_id=models.CharField(max_length=45)
    herbs_name = models.CharField(max_length=10)
    purchases_value = models.FloatField()
    purchases_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'purchase'


class Sale(models.Model):
    sale_id = models.IntegerField(primary_key=True,editable=False)
    customer_id = models.CharField(max_length=15)
    product_name = models.CharField(max_length=10)
    herbs_id=models.IntegerField()
    herbs_name = models.CharField(max_length=10)
    sales_value = models.FloatField()
    order_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sale'


class Sale2(models.Model):
    customer = models.OneToOneField(Sale,on_delete=models.CASCADE, primary_key=True)
    product = models.ForeignKey(Sale,on_delete=models.CASCADE,related_name='products')
    order_time = models.ForeignKey(Sale,on_delete=models.CASCADE, db_column='order_time',related_name='order_times')
    price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sale_2'


class SymptomOfQuestion(models.Model):
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE, primary_key=True,related_name='symptom_questions')
    question_time =models.DateTimeField()
    q1 = models.IntegerField(db_column='Q1', blank=True, null=True)  # Field name made lowercase.
    q2 = models.IntegerField(db_column='Q2', blank=True, null=True)  # Field name made lowercase.
    q3 = models.IntegerField(db_column='Q3', blank=True, null=True)  # Field name made lowercase.
    q4 = models.IntegerField(db_column='Q4', blank=True, null=True)  # Field name made lowercase.
    q5 = models.IntegerField(db_column='Q5', blank=True, null=True)  # Field name made lowercase.
    q6 = models.IntegerField(db_column='Q6', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'symptom of question'
