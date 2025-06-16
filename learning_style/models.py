from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class LearningCharacteristic(models.Model):
    code = models.CharField(max_length=5)
    question = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=[
        ('Visual', 'Visual'),
        ('Auditory', 'Auditory'),
        ('Kinesthetic', 'Kinesthetic'),
    ])
    probability = models.FloatField()

    def __str__(self):
        return f"{self.code} - {self.question}"

# MODEL BARU UNTUK MENYIMPAN HASIL PER USER
class Student(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Pastikan nama unik
    selected_choices = models.TextField(null=True, blank=True)  # Menyimpan pilihan yang dipilih, bisa null
    result = models.CharField(max_length=20, null=True, blank=True)  # Gaya belajar (Visual, Auditory, Kinesthetic), bisa null
    submitted_at = models.DateTimeField(auto_now_add=True)  # Tanggal kuisioner diisi

    def __str__(self):
        return f"{self.name}"
    
