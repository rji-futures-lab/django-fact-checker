from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_safe
from .models import ClaimReview


@require_safe
@login_required
def index(request):
    claim_review_list = ClaimReview.objects.filter(
        published_on__lte=timezone.now()
    ).order_by('-published_on')

    print(claim_review_list.count())

    context = {
        'claim_review_list': claim_review_list,
    }

    return render(request, 'factchecker/index.html', context)


@require_safe
@login_required
def detail(request, claim_review_id):
    context = {
        'claim_review': get_object_or_404(ClaimReview, pk=claim_review_id)
    }
    
    return render(request, 'factchecker/detail.html', context)
