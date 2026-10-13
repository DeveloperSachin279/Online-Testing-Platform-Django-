from django import forms
from exams.models import Subject, Exam, Question

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'slug', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'slug', 'description', 'subject', 'duration_minutes', 'total_marks', 'passing_marks', 'difficulty', 'negative_marking_enabled', 'negative_marks']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'passing_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'negative_marking_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'negative_marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option', 'marks', 'explanation', 'order']
        widgets = {
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'option_a': forms.TextInput(attrs={'class': 'form-control'}),
            'option_b': forms.TextInput(attrs={'class': 'form-control'}),
            'option_c': forms.TextInput(attrs={'class': 'form-control'}),
            'option_d': forms.TextInput(attrs={'class': 'form-control'}),
            'correct_option': forms.Select(attrs={'class': 'form-control'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }
