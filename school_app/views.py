# school_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import StudentSignUpForm, TeacherSignUpForm
from .models import Classroom, Assignment, Submission, Material
from django.contrib.auth import logout
from django.contrib import messages
import os


def home_redirect(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teacher_dashboard')
        else:
            return redirect('student_dashboard')
    else:
        return redirect('login')  # Redirect to the login page if not authenticated



def signup(request):
    return render(request, 'school_app/signup.html')

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('student_dashboard')
    else:
        form = StudentSignUpForm()
    return render(request, 'school_app/student_signup.html', {'form': form})

def teacher_signup(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('teacher_dashboard')
    else:
        form = TeacherSignUpForm()
    return render(request, 'school_app/teacher_signup.html', {'form': form})

@login_required
def student_dashboard(request):
    user=request.user
    classrooms = Classroom.objects.filter(students=user)
    return render(request, 'school_app/student_dashboard.html', {'classrooms': classrooms})


from django.http import HttpResponseBadRequest

@login_required
def join_classroom(request):
    if request.method == 'POST':
        unique_code = request.POST.get('unique_code')
        if unique_code:
            try:
                classroom = Classroom.objects.get(unique_code=unique_code)
                classroom.students.add(request.user)
                return redirect('student_dashboard')
            except Classroom.DoesNotExist:
                return HttpResponseBadRequest("Invalid classroom code.")
    return redirect('student_dashboard')


@login_required
def teacher_dashboard(request):
    classrooms = Classroom.objects.filter(teacher=request.user)
    return render(request, 'school_app/teacher_dashboard.html', {'classrooms': classrooms})

@login_required
def create_classroom(request):
    if request.method == 'POST':
        name = request.POST['name']
        Classroom.objects.create(name=name, teacher=request.user)
        return redirect('teacher_dashboard')
    return render(request, 'school_app/create_classroom.html')

@login_required
def classroom_detail(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)

    # Check if the user is a teacher or a student in this classroom
    if request.user.is_teacher:
        # Teacher's view
        students = classroom.students.all()
        assignments = classroom.assignments.all()
        materials = classroom.materials.all()
        
        return render(request, 'school_app/classroom_detail.html', {
            'classroom': classroom,
            'students': students,
            'assignments': assignments,
            'materials': materials,
        })
    elif request.user in classroom.students.all():
        # Student's view
        assignments = classroom.assignments.all()
        materials = classroom.materials.all()
        return render(request, 'school_app/classroom_detail.html', {
            'classroom': classroom,
            'assignments': assignments,
            'materials': materials,
        })
    else:
        # Neither teacher nor student
        messages.error(request, "You do not have permission to view this classroom.")
        return redirect('student_dashboard' if not request.user.is_teacher else 'teacher_dashboard')
    
    
@login_required
def create_assignment(request, classroom_id):
    classroom = Classroom.objects.get(pk=classroom_id)
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        Assignment.objects.create(classroom=classroom, title=title, description=description)
        return redirect('classroom_detail', pk=classroom_id)
    return render(request, 'school_app/create_assignment.html', {'classroom': classroom})

@login_required
def upload_material(request, classroom_id):
    classroom = Classroom.objects.get(pk=classroom_id)
    if request.method == 'POST':
        file = request.FILES['file']
        Material.objects.create(classroom=classroom, file=file)
        return redirect('classroom_detail', pk=classroom_id)
    return render(request, 'school_app/upload_material.html', {'classroom': classroom})

@login_required
def assignment_detail(request, pk):
    assignment = Assignment.objects.get(pk=pk)
    submissions = Submission.objects.filter(assignment=assignment)
    for submission in submissions:
        submission.filename = os.path.basename(submission.file.name)
    return render(request, 'school_app/assignment_detail.html', {'assignment': assignment, 'submissions': submissions})

@login_required
def submit_assignment(request, assignment_id):
    assignment = Assignment.objects.get(pk=assignment_id)
    if request.method == 'POST':
        file = request.FILES['file']
        Submission.objects.create(assignment=assignment, student=request.user, file=file)
        return redirect('assignment_detail', pk=assignment_id)
    return render(request, 'school_app/submit_assignment.html', {'assignment': assignment})

@login_required
def grade_submission(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)

    if request.method == 'POST':
        grade = request.POST.get('grade', None)
        remark = request.POST.get('remark', '')  # Get the remark from the form

        if grade is not None:
            submission.grade = grade
            submission.remark = remark  # Save the remark
            submission.save()
            return redirect('assignment_detail', pk=submission.assignment.pk)
        else:
            return HttpResponseBadRequest("Grade is missing in the request.")

    return render(request, 'school_app/grade_submission.html', {'submission': submission})


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')



@login_required
def delete_classroom(request, classroom_id):
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    if request.user == classroom.teacher:
        # Delete related materials
        Material.objects.filter(classroom=classroom).delete()
        # Delete related assignments and submissions
        Assignment.objects.filter(classroom=classroom).delete()
        classroom.delete()
        messages.success(request, "Classroom deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this classroom.")
    return redirect('teacher_dashboard')

@login_required
def delete_material(request, material_id):
    material = get_object_or_404(Material, pk=material_id)
    if request.user == material.classroom.teacher:
        material.file.delete()
        material.delete()
        messages.success(request, "Material deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this material.")
    return redirect('classroom_detail', pk=material.classroom.pk)

@login_required
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if request.user == assignment.classroom.teacher:
        Submission.objects.filter(assignment=assignment).delete()
        assignment.delete()
        messages.success(request, "Assignment deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this assignment.")
    return redirect('classroom_detail', pk=assignment.classroom.pk)