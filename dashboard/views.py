from django.shortcuts import render # pyrefly: ignore [missing-import]  # pyright: ignore [reportMissingImports]
from django.contrib.auth.decorators import login_required # pyrefly: ignore [missing-import]  # pyright: ignore [reportMissingImports]
from django.db.models import Count, Avg, Max, Sum # pyrefly: ignore [missing-import]  # pyright: ignore [reportMissingImports]
from results.models import Attempt # pyrefly: ignore [missing-import]  # pyright: ignore [reportMissingImports]
import json # pyrefly: ignore [missing-import]

@login_required
def dashboard(request):
    attempts = Attempt.objects.filter(user=request.user, is_completed=True)
    
    # Global Stats
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
    
    # Recent Activity
    recent_activity = attempts.order_by('-submitted_at')[:5]
    
    # Subject Performance
    subject_stats_raw = attempts.values('exam__subject__name').annotate(
        count=Count('id'),
        avg_score=Avg('percentage'),
        best_score=Max('percentage'),
        total_c=Sum('correct_answers'),
        total_w=Sum('wrong_answers')
    ).order_by('-count')
    
    subject_stats = []
    for s in subject_stats_raw:
        s_att = s['total_c'] + s['total_w']
        s_acc = (s['total_c'] / s_att * 100) if s_att > 0 else 0
        subject_stats.append({
            'name': s['exam__subject__name'],
            'count': s['count'],
            'avg_score': s['avg_score'],
            'best_score': s['best_score'],
            'accuracy': s_acc
        })
        
    # Score Trend (Chronological last 10)
    trend_attempts = list(attempts.order_by('-submitted_at')[:10])
    trend_attempts.reverse()
    
    trend_labels = [a.exam.title[:15] + ('...' if len(a.exam.title) > 15 else '') for a in trend_attempts]
    trend_data = [float(a.percentage) for a in trend_attempts]
    
    # Insights
    insights = []
    if tests_completed == 0:
        insights.append("You haven't completed any tests yet. Head to the Tests section to begin.")
    else:
        insights.append(f"You have completed {tests_completed} tests.")
        if accuracy > 80:
            insights.append("Great job! Your accuracy is very high.")
        elif accuracy < 50:
            insights.append("Try reviewing the explanations after tests to improve your accuracy.")
            
        if len(trend_data) >= 2:
            if trend_data[-1] > trend_data[-2]:
                insights.append("Your latest score was an improvement over the previous one.")
            elif trend_data[-1] < trend_data[-2]:
                insights.append("Your latest score dropped slightly. Keep practicing!")

    context = {
        'tests_completed': tests_completed,
        'avg_score': round(avg_score, 1),
        'best_score': round(best_score, 1),
        'accuracy': round(accuracy, 1),
        'recent_activity': recent_activity,
        'subject_stats': subject_stats,
        'trend_labels_json': json.dumps(trend_labels),
        'trend_data_json': json.dumps(trend_data),
        'insights': insights,
    }
    
    return render(request, 'dashboard/dashboard.html', context)
