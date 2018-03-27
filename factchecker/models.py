from django.conf import settings
from django.db import models
import lipsum
from markdownx.models import MarkdownxField


class BaseModel(models.Model):
    """
    Abstract model with fields common to all fact-checker models.
    """
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(class)s_created",
        related_query_name="%(class)ss_created",
        help_text='Refers to the user who created the object.',
    )
    created_at = models.DateTimeField(
        auto_now=True,
        help_text='Date and time when the object was created.',
    )
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(class)s_modified",
        related_query_name="%(class)ss_modified",
        help_text='Refers to the user who last modified the object.',
    )
    last_modified_at = models.DateTimeField(
        auto_now=True,
        help_text='Date and time when the object was last modified.',
    )

    class Meta:
        abstract = True


class ClaimSource(BaseModel):
    """
    Person, organization or other entity that is the source of a reviewable claim.
    """
    SOURCE_TYPE_CHOICES = (
        ('o', 'Organization'),
        ('p', 'Person'),
    )
    source_type = models.CharField(
        max_length=1,
        choices = SOURCE_TYPE_CHOICES,
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


class ClaimRating(BaseModel):
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
    image = models.ImageField(
        blank=True,
        upload_to='claim-rating-images/',
        # https://docs.djangoproject.com/en/2.0/ref/models/fields/#django.db.models.ImageField.height_field
        # height_field=100, ???
        # width_field=100, ???
        help_text='Image file representing the rating of a claim.',
    )
    emojis = models.CharField(
        max_length=20,
        blank=True,
        help_text='Emojis characters representing the rating of a claim.',
    )

    class Meta:
        verbose_name = 'rating'

    def __str__(self):
        return self.label

    @property
    def css_class(self):
        """
        Return the CSS class to set the label's font color.
        """
        return "%s-color" % self.label.replace(" ", "-").lower()


class Claim(BaseModel):
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

    def __str__(self):
        return "{0} (on {1})".format(self.source.name, self.claimed_on)

    @property
    def is_reviewed(self):
        if self.review:
            return True
        else:
            return False


class ClaimReview(BaseModel):
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
    def body_or_lipsum(self):
        """
        Return the body text (if it exists), otherwise Lorem Ipsum text.
        """
        if not self.body == '':
            return self.body
        else:
            return lipsum.generate_words(100)
