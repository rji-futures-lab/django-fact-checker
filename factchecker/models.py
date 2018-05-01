from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from markdownx.models import MarkdownxField
from phonenumber_field.modelfields import PhoneNumberField


class ClaimSource(models.Model):
    """
    Person, organization or other entity that's a source of reviewable claims.
    """
    SOURCE_TYPE_CHOICES = (
        ('p', 'Person'),
        ('o', 'Organization'),
    )
    source_type = models.CharField(
        max_length=1,
        choices=SOURCE_TYPE_CHOICES,
        help_text="Type of source (e.g., 'Person' or 'Organization').",
    )
    name = models.CharField(
        max_length=300,
        help_text="Name of the source of claim (e.g., 'Donald Trump' or the "
                  "'National Rifle Association').",
    )
    title = models.CharField(
        max_length=300,
        help_text='Title of the source, if it is a person.',
        blank=True,
    )
    image = models.ImageField(
        upload_to='claim-source-images/',
        blank=True,
        # https://docs.djangoproject.com/en/2.0/ref/models/fields/#django.db.models.ImageField.height_field
        # height_field=100, ???
        # width_field=100, ???
        help_text='Image file representing the source.',
    )

    class Meta:
        verbose_name = 'source'

    def __str__(self):
        if self.title != '':
            return '{0.name} ({0.title})'.format(self)
        else:
            return self.name


class ClaimRating(models.Model):
    """
    Possible rating of a claim.
    """
    label = models.CharField(
        max_length=20,
        help_text="Label for the rating (e.g., 'True', 'Mostly True').",
    )
    definition = models.CharField(
        max_length=300,
        blank=True,
        help_text="Definition of the rating.",
    )
    image = models.FileField(
        upload_to='claim-rating-images/',
        blank=True,
        help_text='Image file representing the rating.',
    )
    emojis = models.CharField(
        max_length=20,
        blank=True,
        help_text='Emojis characters representing the rating of a claim.',
    )
    sort_order = models.IntegerField(
        default=0,
        help_text='Order in which this item appears.',
    )

    class Meta:
        verbose_name = 'rating'
        ordering = ['sort_order']

    def __str__(self):
        return self.label

    @property
    def css_class(self):
        """
        Return the CSS class to set the label's font color.
        """
        return "%s-color" % self.label.replace(" ", "-").lower()


class Claim(models.Model):
    source = models.ForeignKey(
        ClaimSource,
        related_name='claims',
        on_delete=models.SET_NULL,
        null=True,
        help_text='Refers to the source of the claim.',
    )
    summary = models.CharField(
        max_length=300,
        help_text='Direct quote or accurate paraphrasing of the claim.',
    )
    body = models.TextField(
        blank=True,
        help_text='Longer definition of the claim (if needed).',
    )
    context_description = models.CharField(
        max_length=300,
        blank=True,
        help_text='Description of the context in which the claim was made.',
    )
    context_url = models.URLField(
        blank=True,
        help_text='Link to the context of the claim (if needed).',
    )
    claimed_on = models.DateField(
        null=True,
        blank=True,
        help_text='Date on which the claim was made.',
    )
    submitter = models.ForeignKey(
        'ClaimSubmitter',
        related_name='claims_submitted',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Refers to the person who submitted the claim.',
    )

    def __str__(self):
        return "{0} (on {1})".format(self.source.name, self.claimed_on)

    @property
    def is_reviewed(self):
        if self.review:
            return True
        else:
            return False


class ClaimReview(models.Model):
    claim = models.OneToOneField(
        Claim,
        related_name='review',
        on_delete=models.CASCADE,
        help_text='Refers to the claim being reviewed.',
    )
    rating = models.ForeignKey(
        ClaimRating,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Refers to the rating assigned to the claim.',
    )
    summary = models.CharField(
        max_length=300,
        blank=True,
        help_text='Short statement summarizing the review of the claim.',
    )
    body = MarkdownxField(
        blank=True,
        help_text='Full narrative of the review, including explanations and '
                  'conclusions surfaced by reporting and research.',
    )
    published_on = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Date and time when the review was/will be published.',
    )

    class Meta:
        verbose_name = 'review'

    def __str__(self):
        return "{0} rated {1} (on {2}).".format(
            self.claim.source.name,
            self.rating.label,
            self.published_on,
        )

    @property
    def is_published(self):
        """Return True if the review has been published."""
        now = timezone.now()
        try:
            return now > self.published_on
        except TypeError:
            return False

    @property
    def published_within_last_24_hours(self):
        """Returns True if the review was published today."""
        if self.is_published:
            now = timezone.now()
            delta = now - self.published_on
            return delta.days == 0
        else:
            return False


class ClaimSubmitter(models.Model):
    name = models.CharField(
        max_length=300,
        help_text='Short statement summarizing the review of the claim.',
    )
    email = models.EmailField(
        blank=True,
        help_text='Email of claim submitter.',
    )
    phone = PhoneNumberField(
        blank=True,
        help_text='Phone number of claim submitter.',
    )

    def __str__(self):
        return self.name

    def clean(self):
        """
        If ClaimSubmitter has neither phone or email, raise ValidationError.
        """
        if not ( bool(self.email) or bool(self.phone) ):
            msg = 'Please provide either a phone or email.'
            raise ValidationError({
                'email': ValidationError(_(msg), code='required'),
                'phone': ValidationError(_(msg), code='required'),
            })
