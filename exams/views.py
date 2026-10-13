from django.shortcuts import render, get_object_or_404, redirect # pyrefly: ignore [missing-import]  # pyright: ignore [reportMissingImports]
from django.contrib.auth.decorators import login_required # pyrefly: ignore [missing-import]  # pyright: ignore [reportMissingImports]
from django.http import JsonResponse # pyrefly: ignore [missing-import]  # pyright: ignore [reportMissingImports]
from django.utils import timezone # pyrefly: ignore [missing-import]  # pyright: ignore [reportMissingImports]
from .models import Exam, Question # pyrefly: ignore [missing-import]  # pyright: ignore [reportMissingImports]
from results.models import Attempt, Answer # pyrefly: ignore [missing-import]  # pyright: ignore [reportMissingImports]
import json
from decimal import Decimal

@login_required
def test_list(request):
    search_query = request.GET.get('search', '')
    exams = Exam.objects.filter(is_published=True)
    if search_query:
        exams = exams.filter(title__icontains=search_query)
    return render(request, 'exams/test_list.html', {'exams': exams, 'search_query': search_query})

@login_required
def test_details(request, slug):
    exam = get_object_or_404(Exam, slug=slug, is_published=True)
    return render(request, 'exams/test_details.html', {'exam': exam})

@login_required
def start_test(request, slug):
    exam = get_object_or_404(Exam, slug=slug, is_published=True)
    # Check if there's an incomplete attempt
    attempt = Attempt.objects.filter(user=request.user, exam=exam, is_completed=False).first()
    if not attempt:
        attempt = Attempt.objects.create(user=request.user, exam=exam)
    return redirect('test_attempt', slug=exam.slug, attempt_id=attempt.id)

@login_required
def test_attempt(request, slug, attempt_id):
    exam = get_object_or_404(Exam, slug=slug, is_published=True)
    attempt = get_object_or_404(Attempt, id=attempt_id, user=request.user, exam=exam)
    
    if attempt.is_completed:
        return redirect('attempt_summary', slug=exam.slug, attempt_id=attempt.id)
    
    # Check time limit
    elapsed = (timezone.now() - attempt.started_at).total_seconds()
    remaining = (exam.duration_minutes * 60) - elapsed
    
    if remaining <= 0:
        return submit_test(request, slug, attempt_id)
        
    questions = exam.questions.all()
    answers = {ans.question_id: ans.selected_option for ans in attempt.answers.all()}
    
    context = {
        'exam': exam,
        'attempt': attempt,
        'questions': questions,
        'answers_json': json.dumps(answers),
        'remaining_seconds': int(remaining),
    }
    return render(request, 'exams/test_attempt.html', context)

@login_required
def save_answer(request, slug, attempt_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
        
    exam = get_object_or_404(Exam, slug=slug)
    attempt = get_object_or_404(Attempt, id=attempt_id, user=request.user, exam=exam)
    
    if attempt.is_completed:
        return JsonResponse({'status': 'error', 'message': 'Test already submitted'})
        
    # Check time
    elapsed = (timezone.now() - attempt.started_at).total_seconds()
    if elapsed > (exam.duration_minutes * 60):
        return JsonResponse({'status': 'error', 'message': 'Time expired'})
        
    data = json.loads(request.body)
    question_id = data.get('question_id')
    selected_option = data.get('selected_option')
    
    question = get_object_or_404(Question, id=question_id, exam=exam)
    
    answer, created = Answer.objects.get_or_create(attempt=attempt, question=question)
    answer.selected_option = selected_option
    answer.save()
    
    return JsonResponse({'status': 'success'})

@login_required
def submit_test(request, slug, attempt_id):
    exam = get_object_or_404(Exam, slug=slug)
    attempt = get_object_or_404(Attempt, id=attempt_id, user=request.user, exam=exam)
    
    if attempt.is_completed:
        return redirect('attempt_summary', slug=exam.slug, attempt_id=attempt.id)
        
    # Finalize attempt
    attempt.is_completed = True
    attempt.submitted_at = timezone.now()
    
    score = Decimal(0)
    correct = 0
    wrong = 0
    unanswered = 0
    
    questions = exam.questions.all()
    total_marks = sum([q.marks for q in questions])
    
    for q in questions:
        ans = attempt.answers.filter(question=q).first()
        if not ans or not ans.selected_option:
            unanswered += 1
        else:
            if ans.selected_option == q.correct_option:
                correct += 1
                score += q.marks
                ans.is_correct = True
                ans.marks_obtained = q.marks
                ans.save()
            else:
                wrong += 1
                if exam.negative_marking_enabled:
                    score -= exam.negative_marks
                ans.is_correct = False
                ans.marks_obtained = -exam.negative_marks if exam.negative_marking_enabled else 0
                ans.save()
                
    attempt.score = score
    attempt.total_marks = total_marks
    attempt.correct_answers = correct
    attempt.wrong_answers = wrong
    attempt.unanswered = unanswered
    if total_marks > 0:
        attempt.percentage = (score / total_marks) * 100
    attempt.save()
    
    return redirect('attempt_summary', slug=exam.slug, attempt_id=attempt.id)
