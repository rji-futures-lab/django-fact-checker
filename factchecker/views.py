from django.conf import settings
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
    ClaimSubmitter,
)


def get_random_skin_tone():
    skin_tones = ('🏻', '🏼', '🏽', '🏾', '🏿',)
    rand_int = randint(0, 4)
    return skin_tones[rand_int]

def get_random_gender():
    genders = ('♀', '♂')
    rand_int = randint(0, 1)
    return genders[rand_int]

def coming_soon(request):
    context = {
        'skin_tone': get_random_skin_tone(),
        'gender': get_random_gender(),
        'url': request.build_absolute_uri(),
        'ogtype': "website",
        'login_url': '%s?next=/' % settings.LOGIN_URL,
        'title': "Coming soon...",
        'description': "This site is still a work in progress. Please check back later.",
    }
    return render(request, 'factchecker/coming_soon.html', context)


@require_safe
@login_required(login_url='/coming-soon/')
@xframe_options_exempt
def index(request):
    claim_review_list = ClaimReview.objects.filter(
        published_on__lte=timezone.now()
    ).order_by('-published_on')

    context = {
        'skin_tone': get_random_skin_tone(),
        'gender': get_random_gender(),
        'url': request.build_absolute_uri(),
        'ogtype': "website",
        'claim_review_list': claim_review_list,
        'title': "Missouri Education Fact Checker",
        'description': "Setting the record straight on education-related issues in Missouri.",
    }

    return render(request, 'factchecker/index.html', context)


@require_safe
@login_required(login_url='/coming-soon/')
@xframe_options_exempt
def detail(request, claim_review_id):
    claim_review = get_object_or_404(ClaimReview, pk=claim_review_id)

    context = {
        'skin_tone': get_random_skin_tone(),
        'gender': get_random_gender(),
        'url': request.build_absolute_uri(),
        'claim_review': claim_review,
        'title': claim_review.claim,
        'ogtype': "article",
    }

    context['description'] = "{0}: {1}".format(
        claim_review.rating.label.upper(),
        claim_review.summary,
    )
    
    return render(request, 'factchecker/detail.html', context)


@require_safe
@login_required(login_url='/coming-soon/')
@xframe_options_exempt
def about(request):
    context = {
        'skin_tone': get_random_skin_tone(),
        'gender': get_random_gender(),
        'url': request.build_absolute_uri(),
        'ratings': ClaimRating.objects.all(),
        'title': "About our project",
        'description': "Learn more about the Missouri Education Fact Checker.",
        'url': request.build_absolute_uri(),
        'ogtype': "article",
    }

    return render(request, 'factchecker/about.html', context)


@xframe_options_exempt
def submit_claim(request):
    context = {
        'title': "Submit a claim",
        'description': "Help us fact check education-related issues in Missouri.",
        'url': request.build_absolute_uri(),
        'ogtype': "website",
    }

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

            submitter_name = form.cleaned_data.get("submitter_name") or ''
            submitter_email = form.cleaned_data.get("submitter_email") or ''
            submitter_phone = form.cleaned_data.get("submitter_phone") or ''

            if submitter_name:
                submitter = ClaimSubmitter.objects.get_or_create(
                    name=submitter_name,
                    email=submitter_email,
                    phone=submitter_phone,
                )[0]
            else:
                submitter = None

            Claim.objects.create(
                source=source,
                claimed_on=form.cleaned_data.get("claimed_on"),
                context_description=form.cleaned_data.get("context_description"),
                context_url=form.cleaned_data.get("context_url"),
                summary=form.cleaned_data.get("claim"),
                body=form.cleaned_data.get("extra"),
                submitter=submitter,
            )

            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ClaimForm()

    context['form'] = form

    return render(request, 'factchecker/submit_claim.html', context)


@xframe_options_exempt
def thanks(request):
    context = {
        'skin_tone': get_random_skin_tone(),
        'url': request.build_absolute_uri(),
        'ogtype': "website",
        'title': "Thanks!",
        'description': "We appreciate the tip. We'll look into this, so check back again later.",
    }
        
    return render(request, 'factchecker/thanks.html', context)
