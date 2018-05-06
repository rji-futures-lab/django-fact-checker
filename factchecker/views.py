from random import randint
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_safe
from django.views.generic import (
    DetailView,
    ListView,
)
from django.views.generic.edit import FormView
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


class TestIconsView(TemplateView):
    template_name ='factchecker/test_icons.html'


@method_decorator(decorators, name='dispatch')
class ComingSoonView(TemplateView):
    """
    Renders the Coming Soon page.
    """

    template_name = "factchecker/coming_soon.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = '%s?next=/' % settings.LOGIN_URL

        return context


@method_decorator(decorators, name='dispatch')
class PublishedClaimReviewListView(ListView):
    """
    Renders a list of published claim reviews.
    """

    queryset = ClaimReview.objects.filter(
        published_on__lte=timezone.now()
    ).order_by('-published_on')


@method_decorator(decorators, name='dispatch')
class PublishedClaimReviewDetailView(DetailView):
    """
    Renders details of a published claim review.
    """

    queryset = ClaimReview.objects.filter(
        published_on__lte=timezone.now()
    )


@method_decorator(decorators, name='dispatch')
class ClaimRatingListView(ListView):
    """
    Renders the about page.
    """

    model = ClaimRating


@method_decorator(decorators, name='dispatch')
class ThanksView(TemplateView):
    """
    Renders the Coming Soon page.
    """
    template_name = "factchecker/thanks.html"


@method_decorator(xframe_options_exempt, name='dispatch')
class ClaimCreateView(FormView):
    """
    """
    template_name = 'factchecker/submit_claim.html'
    form_class = ClaimForm
    success_url = '/thanks/'

    def form_valid(self, form):
        """
        Save ClaimSource, ClaimSubmitter and Claim instances to db.

        Return HttpResponseRedirect to success_url.
        """
        source = form.cleaned_data.get("source")
        if not source.pk:
            source.save()
        
        submitter = form.cleaned_data.get("submitter")
        if isinstance(submitter, ClaimSubmitter):
            if not submitter.pk:
                submitter.save()

        Claim.objects.create(
            source=source,
            submitter=submitter,
            summary=form.cleaned_data.get("claim"),
            body=form.cleaned_data.get("note"),
            context_description=form.cleaned_data.get("context_description"),
            context_url=form.cleaned_data.get("context_url"),
            claimed_on=form.cleaned_data.get("claimed_on"),
        )
        
        return super(ClaimCreateView, self).form_valid(form)
