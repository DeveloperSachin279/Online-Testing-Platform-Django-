from django.contrib import admin
from .models import Attempt, Answer

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'score', 'percentage', 'is_completed', 'submitted_at')
    list_filter = ('is_completed', 'exam__subject', 'exam')
    search_fields = ('user__username', 'exam__title')
    ordering = ('-submitted_at',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_option', 'is_correct', 'marks_obtained')
    list_filter = ('is_correct',)
    search_fields = ('attempt__user__username', 'question__question_text')
