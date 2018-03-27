from random import randint
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_safe
from .models import ClaimReview, ClaimRating
from django.views.decorators.clickjacking import xframe_options_exempt


def get_random_skin_tone():
    skin_tones = ('🏻', '🏼', '🏽', '🏾', '🏿',)
    rand_int = randint(0, 4)
    return skin_tones[rand_int]

def get_random_gender():
    genders = ('♀', '♂')
    rand_int = randint(0, 1)
    return genders[rand_int]


def randomize_emoji(emoji_char):
    zero_width_joiner = chr(int('U+200D'[2:], 16))
    variation_select_char = chr(int('U+FE0F'[2:], 16))

    combine = ''.join([
        emoji_char,
        get_random_skin_tone(),
        zero_width_joiner,
        get_random_gender(),
        variation_select_char
    ])

    print(combine)

    return combine

@require_safe
@login_required
@xframe_options_exempt
def index(request):
    claim_review_list = ClaimReview.objects.filter(
        published_on__lte=timezone.now()
    ).order_by('-published_on')

    context = {
        'claim_review_list': claim_review_list,
        'skin_tone': get_random_skin_tone(),
        'gender': get_random_gender(),
    }

    return render(request, 'factchecker/index.html', context)


@require_safe
@login_required
@xframe_options_exempt
def detail(request, claim_review_id):
    context = {
        'claim_review': get_object_or_404(ClaimReview, pk=claim_review_id),
        'skin_tone': get_random_skin_tone(),
        'gender': get_random_gender(),
    }
    
    return render(request, 'factchecker/detail.html', context)


@require_safe
@login_required
@xframe_options_exempt
def about(request):
    context = {
        'ratings': ClaimRating.objects.all(),
        'skin_tone': get_random_skin_tone(),
        'gender': get_random_gender(),
    }
    return render(request, 'factchecker/about.html', context)
