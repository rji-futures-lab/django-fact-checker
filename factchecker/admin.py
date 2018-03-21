from django.contrib import admin
from django.db import models
from markdownx.admin import MarkdownxModelAdmin
from .models import (
    Claim,
    ClaimRating,
    ClaimReview,
    ClaimSource,
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
        'created_by',
        'created_at',
        'last_modified_by',
        'last_modified_at',
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
        'created_by',
        'created_at',
        'last_modified_by',
        'last_modified_at',
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
        'created_by',
        'created_at',
        'last_modified_by',
        'last_modified_at',
    )
    


@admin.register(ClaimSource)
class ClaimSourceAdmin(admin.ModelAdmin):
    """
    Custom admin for managing ClaimSource instances.
    """
    list_display = (
        'name',
        'created_by',
        'created_at',
        'last_modified_by',
        'last_modified_at',
    )
