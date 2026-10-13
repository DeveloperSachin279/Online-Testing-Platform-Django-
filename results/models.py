from django.db import models
from django.contrib.auth.models import User
from exams.models import Exam, Question

class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total_marks = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    wrong_answers = models.PositiveIntegerField(default=0)
    unanswered = models.PositiveIntegerField(default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_completed = models.BooleanField(default=False)

    @property
    def is_passed(self):
        return self.score >= self.exam.passing_marks

    @property
    def time_taken_seconds(self):
        if self.submitted_at and self.started_at:
            return int((self.submitted_at - self.started_at).total_seconds())
        return 0
        
    @property
    def time_taken_formatted(self):
        seconds = self.time_taken_seconds
        if seconds == 0:
            return "0 sec"
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        parts = []
        if h > 0: parts.append(f"{h} hr")
        if m > 0: parts.append(f"{m} min")
        if s > 0 or not parts: parts.append(f"{s} sec")
        return " ".join(parts)
        
    @property
    def performance_status(self):
        p = float(self.percentage)
        if p >= 90: return 'Excellent'
        if p >= 75: return 'Very Good'
        if p >= 60: return 'Good'
        if p >= 40: return 'Needs Improvement'
        return 'Keep Practicing'

    def __str__(self):
        return f"{self.user.username} - {self.exam.title}"

class Answer(models.Model):
    OPTION_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, choices=OPTION_CHOICES, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        unique_together = ('attempt', 'question')
        
    @property
    def selected_option_text(self):
        if not self.selected_option:
            return "None"
        options = {
            'A': self.question.option_a,
            'B': self.question.option_b,
            'C': self.question.option_c,
            'D': self.question.option_d,
        }
        return options.get(self.selected_option, "Unknown")
        
    @property
    def correct_option_text(self):
        options = {
            'A': self.question.option_a,
            'B': self.question.option_b,
            'C': self.question.option_c,
            'D': self.question.option_d,
        }
        return options.get(self.question.correct_option, "Unknown")

    def __str__(self):
        return f"{self.attempt.user.username} - Q: {self.question.id}"
