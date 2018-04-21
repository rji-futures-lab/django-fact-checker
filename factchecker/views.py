from random import randint
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_safe
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from .forms import ClaimForm
from .models import (
    Claim,
    ClaimRating,
    ClaimReview,
    ClaimSource,
    ClaimSubmitter,
)


decorators = [require_safe, xframe_options_exempt]


@method_decorator(decorators, name='dispatch')
class ComingSoonView(TemplateView):
    """
    Renders the Coming Soon page.
    """

    template_name = "factchecker/coming_soon.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = self.request.build_absolute_uri()
        context['ogtype'] = "website"
        context['login_url'] = '%s?next=/' % settings.LOGIN_URL
        context['title'] = "Coming soon..."
        context['description'] = "This site is still a work in progress. Please check back later."

        return context


@method_decorator(decorators, name='dispatch')
class PublishedClaimReviewListView(LoginRequiredMixin, ListView):
    """
    Renders a list of published claim reviews.
    """

    login_url = '/coming-soon/'
    queryset = ClaimReview.objects.filter(
        published_on__lte=timezone.now()
    ).order_by('-published_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = self.request.build_absolute_uri()
        context['ogtype'] = "website"
        context['title']: "Missouri Education Fact Checker"
        context['description']: "Setting the record straight on education-related issues in Missouri."

        return context


@method_decorator(decorators, name='dispatch')
class PublishedClaimReviewDetailView(LoginRequiredMixin, DetailView):
    """
    Renders details of a published claim review.
    """

    login_url = '/coming-soon/'
    queryset = ClaimReview.objects.filter(
        published_on__lte=timezone.now()
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = self.request.build_absolute_uri()
        context['ogtype'] = "article"
        context['title']: claim_review.claim
        context['description']: "{0}: {1}".format(
            claim_review.rating.label.upper(),
            claim_review.summary,
        )

        return context


@method_decorator(decorators, name='dispatch')
class ClaimRatingListView(LoginRequiredMixin, ListView):
    """
    Renders the about page.
    """
    model = ClaimRating
    login_url = '/coming-soon/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = self.request.build_absolute_uri()
        context['ogtype'] = "article"
        context['title'] = "About our project"
        context['description'] = "Learn more about the Missouri Education Fact Checker.",

        return context


@method_decorator(decorators, name='dispatch')
class ThanksView(TemplateView):
    """
    Renders the Coming Soon page.
    """

    template_name = "factchecker/thanks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = self.request.build_absolute_uri()
        context['ogtype'] = "website"
        context['title'] = "Thanks!"
        context['description'] = "We appreciate the tip. We'll look into this, so check back again later."

        return context


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
