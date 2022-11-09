
from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
class Registration(models.Model):
    First_name = models.CharField(max_length=200)
    Last_name = models.CharField(max_length=200)
    Email = models.EmailField(max_length=200,  null=True)
    Mobile_Number = models.IntegerField(max_length=200, )
    Password = models.CharField(max_length=200)
    Registration_date = models.DateField()
    Image = models.ImageField(upload_to='media')
    Qualification = models.TextField()
    User_role = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.First_name


class Expenses(models.Model):
    Sl_No = models.IntegerField(max_length=200)
    Grocery = models.FloatField(max_length=200)
    Marriage_Expenses = models.FloatField(max_length=200)
    Electricity_Charge = models.FloatField(max_length=200, null = True)
    Water_Charge = models.FloatField(max_length=200)
    Govt_Service_Charges = models.FloatField(max_length=200)
    Other_Expenses = models.FloatField(max_length=200)
    Exp_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null = True)


class Income(models.Model):
    Sl_No = models.IntegerField(max_length=200)
    Salary = models.FloatField(max_length=200, null = True)
    Mutual_Funds = models.FloatField(max_length=200, null = True)
    Tuition = models.FloatField(max_length=200, null = True)
    Total_Income = models.FloatField(max_length=200)
    Inc_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null = True)

class Savingss(models.Model):
    Sl_No = models.IntegerField(max_length=200)
    Month = models.CharField(max_length=200, null = True)
    Bonus = models.IntegerField(max_length=200, null = True)
    Total_Income = models.FloatField(max_length=200, null = True)
    Total_Expenses = models.FloatField(max_length=200, null=True)
    Savings = models.FloatField(max_length=200, null=True)
    Sav_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null = True)


class Requests(models.Model):
    Name = models.CharField(max_length=200)
    Email = models.EmailField()
    User_category = models.CharField(max_length=200)
    Old_password = models.CharField(max_length=200)
    New_password = models.CharField(max_length=200)
    Req_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null = True)
