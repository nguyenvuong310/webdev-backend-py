from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=10, primary_key=True)  

