from django.contrib import admin
from .models import Subject, Exam, Question

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'difficulty', 'duration_minutes', 'total_marks', 'is_published')
    list_filter = ('subject', 'difficulty', 'is_published')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text_short', 'exam', 'correct_option', 'marks', 'order')
    list_filter = ('exam',)
    search_fields = ('question_text',)
    ordering = ('exam', 'order')

    def question_text_short(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Question'
