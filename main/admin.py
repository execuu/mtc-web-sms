from django.contrib import admin
from .models import Student, Coaches, Strand, Subject, Attendance, Attendance_List

# Register your models here.
admin.site.register(Strand)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Coaches)
admin.site.register(Attendance)
admin.site.register(Attendance_List)