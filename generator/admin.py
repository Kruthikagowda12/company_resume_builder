# from django.contrib import admin
from django.contrib import admin
from .models import Employee, Project, EmployeeProjectMapping

admin.site.register(Employee)
admin.site.register(Project)
admin.site.register(EmployeeProjectMapping)
# Register your models here.
