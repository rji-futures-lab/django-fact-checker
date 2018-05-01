from django.contrib import admin
from django.db import models
from markdownx.admin import MarkdownxModelAdmin
from .models import (
    Claim,
    ClaimRating,
    ClaimReview,
    ClaimSource,
    ClaimSubmitter,
)


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    """
    Custom admin for managing Claim instances.
    """
    list_display = (
        'source',
        'summary',
        'context_description',
        'review',
        'claimed_on',
        'submitter',
    )


@admin.register(ClaimSubmitter)
class ClaimSubmitterAdmin(admin.ModelAdmin):
    """
    Custom admin for managing ClaimSubmitter instances.
    """
    list_display = (
        'name',
        'email',
        'phone',
    )


@admin.register(ClaimRating)
class ClaimRatingAdmin(admin.ModelAdmin):
    """
    Custom admin for managing ClaimRating instances.
    """
    list_display = (
        'label',
        'emojis',
        'definition',
        'sort_order',
        'image',
    )


@admin.register(ClaimReview)
class ClaimReviewAdmin(MarkdownxModelAdmin):
    """
    Custom admin for managing ClaimReview instances.
    """
    list_display = (
        'claim',
        'rating',
        'summary',
        'published_on',
    )


@admin.register(ClaimSource)
class ClaimSourceAdmin(admin.ModelAdmin):
    """
    Custom admin for managing ClaimSource instances.
    """
    list_display = (
        'source_type',
        'name',
    )
