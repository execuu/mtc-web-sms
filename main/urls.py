from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path("", views.home, name="home"),
    path("students/", views.student_list, name='students'),
    path('<int:student_id>/', views.view_student, name='view_student'),
    path('add_student/', views.add_student, name='add_student'),
    path('edit_student/<int:id>/', views.edit_student, name='edit_student'),
    path('delete_student/<int:id>/', views.delete_student, name='delete_student'),
    path('coaches/', views.coaches_list, name='coaches'),
    path('view_coaches/<int:id>', views.view_coaches, name='view_coaches'),
    path('add_coaches/', views.add_coach, name='add_coaches'),
    path('edit_coaches/<int:id>/', views.edit_coaches, name='edit_coaches'),
    path('delete_coaches/<int:id>/', views.delete_coaches, name='delete_coaches'),
    path('strands_subjects/', views.strands_subjects, name='strands_subjects'),
    path('attendance/', views.attendance, name='attendances'),
    path('attendance_login/', views.attendance_login, name='attendance_login'),
    path('attendance_submit/', views.attendance_submit, name='attendance_submit'),
    path('attendance_list/', views.attendance_list, name='attendance_list'),
]
