from django.shortcuts import render, get_object_or_404, redirect # pyrefly: ignore [missing-import]  # pyright: ignore [reportMissingImports]
from django.core.paginator import Paginator # pyrefly: ignore [missing-import]  # pyright: ignore [reportMissingImports]
from django.contrib.auth.decorators import user_passes_test # pyrefly: ignore [missing-import]  # pyright: ignore [reportMissingImports]
from django.core.exceptions import PermissionDenied # pyrefly: ignore [missing-import]  # pyright: ignore [reportMissingImports]
from django.contrib import messages # pyrefly: ignore [missing-import]  # pyright: ignore [reportMissingImports]
from django.contrib.auth.models import User # pyrefly: ignore [missing-import]  # pyright: ignore [reportMissingImports]
from exams.models import Subject, Exam, Question # pyrefly: ignore [missing-import]  # pyright: ignore [reportMissingImports]
from results.models import Attempt # pyrefly: ignore [missing-import]  # pyright: ignore [reportMissingImports]
from .forms import SubjectForm, ExamForm, QuestionForm # pyrefly: ignore [missing-import]  # pyright: ignore [reportMissingImports]

def is_admin(user):
    if not user.is_authenticated:
        return False
    if not user.is_staff:
        raise PermissionDenied
    return True

@user_passes_test(is_admin)
def dashboard(request):
    total_students = User.objects.filter(is_staff=False).count()
    total_tests = Exam.objects.count()
    total_questions = Question.objects.count()
    total_attempts = Attempt.objects.count()
    
    recent_students = User.objects.filter(is_staff=False).order_by('-date_joined')[:5]
    recent_attempts = Attempt.objects.filter(is_completed=True).order_by('-submitted_at')[:5]
    recent_tests = Exam.objects.order_by('-created_at')[:5]
    
    context = {
        'total_students': total_students,
        'total_tests': total_tests,
        'total_questions': total_questions,
        'total_attempts': total_attempts,
        'recent_students': recent_students,
        'recent_attempts': recent_attempts,
        'recent_tests': recent_tests,
    }
    return render(request, 'admin_panel/dashboard.html', context)

# --- Subjects ---
@user_passes_test(is_admin)
def subject_list(request):
    subjects = Subject.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/subject_list.html', {'subjects': subjects})

@user_passes_test(is_admin)
def subject_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject created successfully.')
            return redirect('admin_subject_list')
    else:
        form = SubjectForm()
    return render(request, 'admin_panel/subject_form.html', {'form': form, 'title': 'Create Subject'})

@user_passes_test(is_admin)
def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject updated successfully.')
            return redirect('admin_subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'admin_panel/subject_form.html', {'form': form, 'title': 'Edit Subject'})

@user_passes_test(is_admin)
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully.')
        return redirect('admin_subject_list')
    return render(request, 'admin_panel/confirm_delete.html', {'object': subject, 'cancel_url': 'admin_subject_list'})

# --- Exams ---
@user_passes_test(is_admin)
def exam_list(request):
    exams = Exam.objects.all().order_by('-created_at')
    paginator = Paginator(exams, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_panel/exam_list.html', {'exams': page_obj})

@user_passes_test(is_admin)
def exam_create(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save()
            messages.success(request, 'Exam created successfully.')
            return redirect('admin_exam_detail', pk=exam.pk)
    else:
        form = ExamForm()
    return render(request, 'admin_panel/exam_form.html', {'form': form, 'title': 'Create Exam'})

@user_passes_test(is_admin)
def exam_update(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam updated successfully.')
            return redirect('admin_exam_detail', pk=exam.pk)
    else:
        form = ExamForm(instance=exam)
    return render(request, 'admin_panel/exam_form.html', {'form': form, 'title': 'Edit Exam'})

@user_passes_test(is_admin)
def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        exam.delete()
        messages.success(request, 'Exam deleted successfully.')
        return redirect('admin_exam_list')
    return render(request, 'admin_panel/confirm_delete.html', {'object': exam, 'cancel_url': 'admin_exam_list'})

@user_passes_test(is_admin)
def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    questions = exam.questions.all().order_by('order', 'id')
    return render(request, 'admin_panel/exam_detail.html', {'exam': exam, 'questions': questions})

@user_passes_test(is_admin)
def exam_publish_toggle(request, pk):
    if request.method == 'POST':
        exam = get_object_or_404(Exam, pk=pk)
        if not exam.is_published:
            # Validate before publishing
            if exam.questions.count() == 0:
                messages.error(request, 'Cannot publish exam without any questions.')
                return redirect('admin_exam_detail', pk=exam.pk)
            # More validation can be added here if needed
            exam.is_published = True
            messages.success(request, 'Exam published successfully.')
        else:
            exam.is_published = False
            messages.success(request, 'Exam unpublished successfully.')
        exam.save()
    return redirect('admin_exam_detail', pk=pk)

# --- Questions ---
@user_passes_test(is_admin)
def question_create(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.exam = exam
            q.save()
            messages.success(request, 'Question added successfully.')
            return redirect('admin_exam_detail', pk=exam.pk)
    else:
        form = QuestionForm(initial={'order': exam.questions.count() + 1})
    return render(request, 'admin_panel/question_form.html', {'form': form, 'exam': exam, 'title': 'Add Question'})

@user_passes_test(is_admin)
def question_update(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question updated successfully.')
            return redirect('admin_exam_detail', pk=question.exam.pk)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'admin_panel/question_form.html', {'form': form, 'exam': question.exam, 'title': 'Edit Question'})

@user_passes_test(is_admin)
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    exam_id = question.exam.pk
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted successfully.')
        return redirect('admin_exam_detail', pk=exam_id)
    return render(request, 'admin_panel/confirm_delete.html', {'object': question, 'cancel_url_dynamic': 'admin_exam_detail', 'cancel_arg': exam_id})

# --- Students ---
@user_passes_test(is_admin)
def student_list(request):
    search_query = request.GET.get('search', '')
    students = User.objects.filter(is_staff=False).order_by('-date_joined')
    if search_query:
        students = students.filter(username__icontains=search_query)
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_panel/student_list.html', {'students': page_obj, 'search_query': search_query})

@user_passes_test(is_admin)
def student_toggle_active(request, pk):
    if request.method == 'POST':
        student = get_object_or_404(User, pk=pk, is_staff=False)
        student.is_active = not student.is_active
        student.save()
        messages.success(request, f"Student {'activated' if student.is_active else 'deactivated'} successfully.")
    return redirect('admin_student_list')
