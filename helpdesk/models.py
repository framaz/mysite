from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear


class Department(models.Model):
    name = models.CharField(max_length=100)
    head = models.ForeignKey('auth.User', null=True, on_delete=models.CASCADE, related_name="head")

    def __str__(self):
        return self.name + " " + str(self.id)


class Ticket(models.Model):
    requestor = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="requestor")
    worker = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name="worker")
    theme = models.CharField(max_length=100, default="")
    targeted_department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name="targeted_department")
    place = models.CharField(max_length=100, default="")
    priority = models.IntegerField(default="0")  # 0-Низкий 1-Средний 2-Высокий
    details = models.CharField(max_length=1000, default="")
    pub_date = models.DateTimeField('date published')
    exp_date = models.DateTimeField('expiration date')
    finished = models.BooleanField(default="False")
    deleted = models.BooleanField(default="False")
    chat = models.TextField(default="")

    def __str__(self):
        return self.theme + " " + str(self.id)

    def nice_exp_date(this):
        return ExtractDay(this.exp_date) + "/" + ExtractMonth(this.exp_date) + "/" + ExtractYear(this.exp_date)


class EmployeesInDepartments(models.Model):
    person = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="person")
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name="department")

    def __str__(self):
        return self.person.first_name + self.person.last_name + " X " + self.department.name + " " + str(self.id)


class QuestionsAndAnswers(models.Model):
    question = models.CharField(max_length=1000, default="")
    answer = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.question + " " + str(self.id)


class Message(models.Model):
    sender = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="sender")
    reciver = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="reciver")
    text = models.CharField(max_length=1000, default="")
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    deleted = models.BooleanField(default="False")
    status = models.CharField(max_length=20, default="Отправлено")
    date = models.DateTimeField('date')

# buh 1w2e3r4t
# tech 1w2e3r4t
# buhxtech 1w2e3r4t
# noone 1w2e3r4t
