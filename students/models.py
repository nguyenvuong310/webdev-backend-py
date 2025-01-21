from django.db import models

class Student(models.Model):
    class Meta:
        db_table = 'students'
    id = models.CharField(max_length=10, primary_key=True)
