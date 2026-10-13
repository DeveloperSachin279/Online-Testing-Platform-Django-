from django.db import models
from django.utils.text import slugify

class Subject(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Exam(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    duration_minutes = models.PositiveIntegerField()
    total_marks = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    passing_marks = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    negative_marking_enabled = models.BooleanField(default=False)
    negative_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='Medium')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    OPTION_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_option = models.CharField(max_length=1, choices=OPTION_CHOICES)
    marks = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    explanation = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Q: {self.question_text[:50]}"
