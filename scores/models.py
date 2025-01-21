from django.db import models
from students.models import Student

class Score(models.Model):
    class Meta:
        db_table = 'scores'
    
    math = models.FloatField(null=True, blank=True)
    literature = models.FloatField(null=True, blank=True)
    language = models.FloatField(null=True, blank=True)
    physics = models.FloatField(null=True, blank=True)
    chemistry = models.FloatField(null=True, blank=True)
    biology = models.FloatField(null=True, blank=True)
    history = models.FloatField(null=True, blank=True)
    geography = models.FloatField(null=True, blank=True)
    civics = models.FloatField(null=True, blank=True)
    foreign_language_code = models.CharField(max_length=5, null=True, blank=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='profile')
