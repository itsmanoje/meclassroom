# school_app/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)



# school_app/models.py
from django.db import models
from django.conf import settings

#class Classroom(models.Model):
#    name = models.CharField(max_length=100)
#    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classrooms') #settings.AUTH_USER_MODEL
#    students = models.ManyToManyField(User, related_name='enrolled_classrooms', blank=True)

import random
import string

class Classroom(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classrooms')
    students = models.ManyToManyField(User, related_name='enrolled_classrooms', blank=True)
    unique_code = models.CharField(max_length=6, unique=True, default='')

    class Meta:
        unique_together = ('teacher', 'name')

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = self._generate_unique_code()
        super().save(*args, **kwargs)

    def _generate_unique_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class Meta:
    unique_together = ('teacher', 'name')

class Material(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='materials')
    file = models.FileField(upload_to='materials/')
    created_at = models.DateTimeField(auto_now_add=True)

class Assignment(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    grade = models.IntegerField(null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
