from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date


class Daily(models.Model):
    weekly = models.IntegerField(default = 0)
    extra_days = models.IntegerField(default = 0)
    transportation = models.IntegerField(default = 0)
    cleaning_help = models.IntegerField(default = 0)
    gas = models.IntegerField(default = 0)
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    date = models.DateField(default=timezone.now)
    

    def sum_of_daily(self):
        return self.weekly + self.extra_days + self.transportation + self.cleaning_help + self.gas

    

class Monthly(models.Model):
    mortgage = models.IntegerField(default = 0)
    vaad_bayit = models.IntegerField(default = 0)
    internet_tel = models.IntegerField(default = 0)
    cell_phone = models.IntegerField(default = 0)
    life_insurance = models.IntegerField(default = 0)
    health_insurance = models.IntegerField(default = 0)
    home_insurance = models.IntegerField(default = 0)
    therapy = models.IntegerField(default = 0)
    tuters = models.IntegerField(default = 0)
    children_savings = models.IntegerField(default = 0)
    bank_fees = models.IntegerField(default = 0)
    monthly_loan = models.IntegerField(default = 0)
    charity = models.IntegerField(default = 0)
    car_insurance_chova = models.IntegerField(default = 0)
    car_insurance_makif = models.IntegerField(default = 0)
    extracurricular_activity = models.IntegerField(default = 0)
    tuition = models.IntegerField(default = 0)
    kids_transportation = models.IntegerField(default = 0)
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    date = models.DateField(default=timezone.now)


    def sum_of_monthly_expenses(self):
        self.total_monthly_expenses = self.mortgage + self.vaad_bayit + self.internet_tel + self.cell_phone + self.life_insurance + self.health_insurance + self.home_insurance + self.therapy + self.tuters + self.children_savings + self.bank_fees + self.monthly_loan + self.charity + self.car_insurance_chova+ self.car_insurance_makif + self.extracurricular_activity + self.tuition + self.kids_transportation
        return self.total_monthly_expenses


class Annual(models.Model):
    property_tax = models.IntegerField(default = 0)
    water = models.IntegerField(default = 0)
    gas = models.IntegerField(default = 0)
    electric = models.IntegerField(default = 0)
    holidays = models.IntegerField(default = 0)
    dental = models.IntegerField(default = 0)
    eyecare = models.IntegerField(default = 0)
    alternative_medicine = models.IntegerField(default = 0)
    kids_gifts = models.IntegerField(default = 0)
    couples_gifts = models.IntegerField(default = 0)
    general_gifts = models.IntegerField(default = 0)
    school_supplies = models.IntegerField(default = 0)
    membership_fees = models.IntegerField(default = 0)
    day_trips = models.IntegerField(default = 0)
    couples_vacation = models.IntegerField(default = 0)
    family_vacation = models.IntegerField(default = 0)
    car_registration = models.IntegerField(default = 0)
    car_test = models.IntegerField(default = 0)
    car_repairs = models.IntegerField(default = 0)
    extracurricular_activity = models.IntegerField(default = 0)
    water_filter = models.IntegerField(default = 0)
    extra_income = models.IntegerField(default = 0)
    other_school_fees = models.IntegerField(default = 0)
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    date = models.DateField(default=timezone.now)



    # def __str__(self):
    #     return f'{self}'


    # def __repr__(self):
    #     return f'{self}'


    def sum_of_annual_expenses(self):
        self.total_annual_expenses = self.property_tax + self.water + self.gas + self.electric + self.holidays + self.dental + self.eyecare + self.alternative_medicine + self.kids_gifts + self.couples_gifts + self.general_gifts + self.school_supplies + self.membership_fees + self.day_trips + self.couples_vacation + self.family_vacation + self.car_registration + self.car_test + self.car_repairs + self.extracurricular_activity + self.water_filter + self.extra_income + self.other_school_fees
        return self.total_annual_expenses


class Additional_expenses(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)
    category = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    date = models.DateField(default=timezone.now)



class MoneySpent(models.Model):
    name = models.CharField(default='expense', max_length=100)
    spent = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    date = models.DateField(default=timezone.now)
    # auto_add_now=True fix at home


class Budget(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    date = models.DateField(default=timezone.now)
    

class Bot(models.Model):
    text = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    date = models.DateField(default=timezone.now)

