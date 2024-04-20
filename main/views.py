from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib import messages, auth
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Student, Coaches, Strand, Attendance, Attendance_List
from .forms import StudentForm, CoachForm, CustomAuthenticationForm, AttListLogin

# Create your views here.

User = get_user_model()

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

def home(request):
    return render(request, 'main/home.html')

@login_required
def student_list(request):
    if request.method == 'POST':
        form = Student(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = Student()
    return render(request, 'main/student_list.html' , {
        'students': Student.objects.all()
    })

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                student = form.save(commit=False)
                student.save()
                messages.success(request, f"Student: {student.firstName} {student.lastName} has been added successfully!")
            except IntegrityError:
                messages.error(request, 'Failed to add student. Student number already exists.')
            return redirect('students')
    else:
        form = StudentForm()

    return render(request, 'main/add.html', {'form': form})

def edit_student(request, id):
    student = Student.objects.get(pk=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f"Student: {student.firstName} {student.lastName} has been updated successfully!")
            return redirect('students')
    else:
        form = StudentForm(instance=student)

    context = {
        'form': form,
        'student': student
    }

    html_form = render_to_string('main/editStudent.html', context, request=request)
    return JsonResponse({'html_form': html_form})

def delete_student(request, id):
    if request.method == 'POST':
        student = Student.objects.get(pk=id)
        student.delete()
        messages.success(request, f"Student: {student.firstName} {student.lastName} has been deleted successfully!")
    return HttpResponseRedirect(reverse('students'))
        
def view_student(request, student_id):
    student = Student.objects.get(pk=student_id)
    return render(request, 'main/view_student.html', {'student': student})

@login_required
def coaches_list(request):
    return render(request, 'main/coaches_list.html' , {
        'coaches': Coaches.objects.all()
    })

def add_coach(request):
    if request.method == 'POST':
        form = CoachForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                coach = form.save(commit=False)
                coach.save()
                messages.success(request, f"Coach: {coach.firstName} {coach.lastName} has been added successfully!")
            except IntegrityError:
                messages.error(request, 'Failed to add coach. Coach already exists.')
            return redirect('coaches')
    else:
        form = CoachForm()

    return render(request, 'main/addCoaches.html', {'form': form})

def edit_coaches(request, id):
    coaches = Coaches.objects.get(pk=id)
    if request.method == 'POST':
        form = CoachForm(request.POST, request.FILES, instance=coaches)
        if form.is_valid():
            form.save()
            messages.success(request, f"Coach: {coaches.firstName} {coaches.lastName} has been updated successfully!")
            return redirect('coaches')
    else:
        form = CoachForm(instance=coaches)

    context = {
        'form': form,
        'coaches': coaches
    }

    html_form = render_to_string('main/editCoach.html', context, request=request)
    return JsonResponse({'html_form': html_form})

def delete_coaches(request, id):
    if request.method == 'POST':
        coaches = Coaches.objects.get(pk=id)
        coaches.delete()
        messages.success(request, f"Coach: {coaches.firstName} {coaches.lastName} has been deleted successfully!")
    return HttpResponseRedirect(reverse('coaches'))

def view_coaches(request, id):
    coaches = Coaches.objects.get(pk=id)
    return HttpResponseRedirect(reverse['index'])

def strands_subjects(request):
    return render(request, 'main/strandAndSubjects.html' , {
        'strands': Strand.objects.all()
    })

def attendance(request):
    attendance_qr_codes = Attendance.objects.all()
    return render(request, 'main/attendance.html', {'attendance_qr_codes': attendance_qr_codes})

@login_required
def attendance_login(request):
    try:
        att_list = Attendance.objects.get()
    except Exception as e:
        raise e
    context = {
        'att_list': att_list
    }
    return render(request, 'main/attendance_form.html', context)


def attendance_list(request):
    try:
        att_list = Attendance.objects.get()
    except Exception as e:
        raise e

    student_list = Attendance_List.objects.order_by('-created_at').filter(qrcode_id=att_list.id)
    count = student_list.count()
    context = {
        'att_list': att_list,
        'student_list': student_list,
        'count':count,
    }
    return render(request, 'main/attendance_list.html' , {
        'students': Student.objects.all(),
        'context': context
    })

@login_required
def attendance_submit(request,):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form=AttListLogin(request.POST)
        if form.is_valid():
            password = form.cleaned_data['loginid']
            user = authenticate(request, password=password)
            newstudent = Attendance_List()
            if  request.user.password == password:
                newstudent.loginid = password
                newstudent.user = user
                newstudent.save()
                messages.success(request, 'Successfully Logged on the Attendance List')
                return redirect('attendance_list')
            else:
                messages.warning(request, 'Your Id Number Incorrect')
                return redirect(url)

    return render(request, 'main/attendance_form.html')
