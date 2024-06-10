from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/student/', views.student_signup, name='student_signup'),
    path('signup/teacher/', views.teacher_signup, name='teacher_signup'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/create_classroom/', views.create_classroom, name='create_classroom'),
    path('classroom/<int:pk>/', views.classroom_detail, name='classroom_detail'),  # Correctly defined URL
    path('classroom/<int:classroom_id>/create_assignment/', views.create_assignment, name='create_assignment'),
    path('classroom/<int:classroom_id>/upload_material/', views.upload_material, name='upload_material'),
    path('assignment/<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    path('submission/<int:submission_id>/grade/', views.grade_submission, name='grade_submission'),
    path('logout/', views.logout_user, name='logout'),
    path('delete_classroom/<int:classroom_id>/', views.delete_classroom, name='delete_classroom'),
    path('delete_material/<int:material_id>/', views.delete_material, name='delete_material'),
    path('delete_assignment/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),
    path('join-classroom/', views.join_classroom, name='join_classroom'),
]
