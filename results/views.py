from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Attempt
from exams.models import Exam

@login_required
def result_list(request):
    attempts = Attempt.objects.filter(user=request.user, is_completed=True).order_by('-submitted_at')
    paginator = Paginator(attempts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'results/result_list.html', {'attempts': page_obj})

@login_required
def attempt_summary(request, slug, attempt_id):
    exam = get_object_or_404(Exam, slug=slug)
    attempt = get_object_or_404(Attempt, id=attempt_id, user=request.user, exam=exam)
    return render(request, 'results/attempt_summary.html', {'attempt': attempt, 'exam': exam})

@login_required
def detailed_result(request, attempt_id):
    attempt = get_object_or_404(Attempt, id=attempt_id, user=request.user, is_completed=True)
    # Prefetch answers and related questions to optimize query
    answers = attempt.answers.select_related('question').order_by('question__order', 'question__id')
    return render(request, 'results/detailed_result.html', {'attempt': attempt, 'answers': answers})
