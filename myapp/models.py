# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Customer(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=45)
    customer_name = models.CharField(max_length=10)
    sex = models.CharField(max_length=10)
    age = models.IntegerField()
    line_id = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'


class Employee(models.Model):
    account = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'employee'


class HerbStock(models.Model):
    herbs_id = models.IntegerField(primary_key=True)
    herbs_name = models.OneToOneField('Purchase', on_delete=models.CASCADE)
    current_stock = models.FloatField()

    class Meta:
        managed = False
        db_table = 'herb_stock'


class Purchase(models.Model):
    purchases_id = models.IntegerField(primary_key=True,editable=False)
    herbs_name = models.CharField(max_length=10)
    purchases_value = models.FloatField()
    purchases_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'purchase'


class Sale(models.Model):
    customer = models.OneToOneField('HerbStock', on_delete=models.CASCADE, primary_key=True)
    product_id = models.IntegerField()
    herbs_id = models.IntegerField()
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
    question_time = models.ForeignKey(Sale,on_delete=models.CASCADE, db_column='question_time',related_name='questions')
    q1 = models.IntegerField(db_column='Q1', blank=True, null=True)  # Field name made lowercase.
    q2 = models.IntegerField(db_column='Q2', blank=True, null=True)  # Field name made lowercase.
    q3 = models.IntegerField(db_column='Q3', blank=True, null=True)  # Field name made lowercase.
    q4 = models.IntegerField(db_column='Q4', blank=True, null=True)  # Field name made lowercase.
    q5 = models.IntegerField(db_column='Q5', blank=True, null=True)  # Field name made lowercase.
    q6 = models.IntegerField(db_column='Q6', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'symptom of question'
