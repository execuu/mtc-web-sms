from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator
from .models import *

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class StudentForm(forms.ModelForm):
    
    school_year_choices = [(choice[0], choice[1]) for choice in SCHOOL_YEAR_CHOICES]
    # strand_choices = [(choice[0], choice[1]) for choice in STRAND]
    grade_level_choices = [(choice[0], choice[1]) for choice in grade_level]

    school_year = forms.ChoiceField(choices=school_year_choices, initial='2023-24', widget=forms.Select(attrs={'class': 'form-control'}), label='School Year')
    LRN = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Learners Reference Number')
    firstName = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}), label='First Name')
    lastName = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Last Name')
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Email')
    addrs = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Address')
    # strand = forms.ChoiceField(choices=strand_choices, widget=forms.Select(attrs={'class': 'form-control'}), label='Strand')
    gradeLevel = forms.ChoiceField(choices=grade_level_choices, widget=forms.Select(attrs={'class': 'form-control'}), label='Grade Level')
    section = forms.CharField(max_length=3, validators=[RegexValidator(r'^\d{1,3}$')], widget=forms.TextInput(attrs={'class': 'form-control'}), label='Section')

    class Meta:
        model = Student
        fields = '__all__'  
        labels = {
            'school_year': 'School Year',
            'LRN': 'Learners Reference Number',
            'firstName': 'First Name',
            'lastName': 'Last Name',
            'email': 'Email',
            'addrs': 'Address',
            'strand': 'Strand',
            'gradeLevel': 'Grade Level',
            'section': 'Section',
            'picture': 'Picture',
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })

class CoachForm(forms.ModelForm):

    class CoachForm(forms.ModelForm):
        cpNum = forms.CharField(max_length=12, validators=[RegexValidator(r'^\d{1,12}$')], required=False)

    class Meta:
        model = Coaches
        fields = ['firstName', 'middleName', 'lastName', 'email', 'addrs', 'cpNum', 'strand', 'subject']
        labels = {
            'firstName': 'First Name',
            'middleName': 'Middle Name',
            'lastName': 'Last Name',
            'email': 'Email',
            'addrs': 'Address',
            'cpNum': 'Contact Number',
            'strand': 'Academic Strand',
            'subject': 'Subject(s)'
        }

    def __init__(self, *args, **kwargs):
        super(CoachForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })


class AttListLogin(forms.ModelForm):
    class Meta:
        model = Attendance_List
        fields = ['loginid']