from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_safe
from random import randint
from .forms import ClaimForm
from .models import (
    Claim,
    ClaimRating,
    ClaimReview,
    ClaimSource,
)


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


@xframe_options_exempt
def submit_claim(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ClaimForm(request.POST)
        
        if form.is_valid():
            source = form.cleaned_data.get("source") or ''
            if source == '':
                try:
                    source = ClaimSource.objects.get(
                        source_type=form.cleaned_data.get("source_type"),
                        name=form.cleaned_data.get("source_name"),
                        title=form.cleaned_data.get("source_title"),
                    )
                except:
                    source = ClaimSource.objects.create(
                        source_type=form.cleaned_data.get("source_type"),
                        name=form.cleaned_data.get("source_name"),
                        title=form.cleaned_data.get("source_title"),
                    )

            Claim.objects.create(
                source=source,
                claimed_on=form.cleaned_data.get("claimed_on"),
                context_description=form.cleaned_data.get("context_description"),
                context_url=form.cleaned_data.get("context_url"),
                summary=form.cleaned_data.get("claim"),
                body=form.cleaned_data.get("extra"),
            )

            return HttpResponseRedirect('/thanks/')
        
        # else?

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ClaimForm()

    return render(request, 'factchecker/submit-claim.html', {'form': form})


@xframe_options_exempt
def thanks(request):
    return render(request, 'factchecker/thanks.html')
