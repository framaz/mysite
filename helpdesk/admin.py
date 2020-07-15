from django.contrib import admin
from .models import Department, Ticket, EmployeesInDepartments, QuestionsAndAnswers, Message


class DepartmentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Ticket, DepartmentAdmin)
admin.site.register(EmployeesInDepartments, DepartmentAdmin)
admin.site.register(QuestionsAndAnswers, DepartmentAdmin)
admin.site.register(Message, DepartmentAdmin)
# Register your models here.
