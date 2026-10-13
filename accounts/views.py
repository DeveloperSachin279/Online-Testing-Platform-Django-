from django.shortcuts import render, redirect # pyrefly: ignore [missing-import]
from django.contrib.auth.forms import UserCreationForm # pyrefly: ignore [missing-import]
from django.contrib.auth.decorators import login_required # pyrefly: ignore [missing-import]
from django.contrib import messages # pyrefly: ignore [missing-import]
from django.db.models import Avg, Max, Sum # pyrefly: ignore [missing-import]
from results.models import Attempt

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'accounts/landing.html', {'public_page': True})

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form, 'public_page': True})

@login_required
def profile(request):
    attempts = Attempt.objects.filter(user=request.user, is_completed=True)
    tests_completed = attempts.count()
    
    aggs = attempts.aggregate(
        avg_score=Avg('percentage'),
        best_score=Max('percentage'),
        total_correct=Sum('correct_answers'),
        total_wrong=Sum('wrong_answers')
    )
    
    avg_score = aggs['avg_score'] or 0
    best_score = aggs['best_score'] or 0
    total_correct = aggs['total_correct'] or 0
    total_wrong = aggs['total_wrong'] or 0
    total_attempted = total_correct + total_wrong
    accuracy = (total_correct / total_attempted * 100) if total_attempted > 0 else 0
    
    latest_attempt = attempts.order_by('-submitted_at').first()
    
    context = {
        'tests_completed': tests_completed,
        'avg_score': round(avg_score, 1),
        'best_score': round(best_score, 1),
        'accuracy': round(accuracy, 1),
        'latest_attempt': latest_attempt,
    }
    return render(request, 'accounts/profile.html', context)
