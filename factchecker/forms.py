from django import forms
from django.core.exceptions import ValidationError
from bootstrap_datepicker.widgets import DatePicker
from phonenumber_field.formfields import PhoneNumberField
from .models import ClaimSource, ClaimSubmitter


class ClaimForm(forms.Form):
    source = forms.ModelChoiceField(
        label='Name of person or organization',
        queryset=ClaimSource.objects.all(),
        help_text='Can\'t find who you\'re looking for? Click "Add New".',
    )
    source_type = forms.ChoiceField(
        required=False,
        label='Type',
        choices=ClaimSource.SOURCE_TYPE_CHOICES,
        help_text='We prefer claims attributed to specific people. Otherwise, '
                  'select "Organization".',
    )
    source_name = forms.CharField(
        required=False,
        label='Name',
        max_length=300,
        help_text='If attributed to a person, please provide their first and '
                  'last names.',
    )
    source_title = forms.CharField(
        required=False,
        label='Title',
        max_length=300,
        help_text='Please include the person\'s current title, if known.',
    )
    claimed_on = forms.DateField(
        required=False,
        label='Claimed on',
        widget=DatePicker(
            options={
                'todayBtn': "linked",
                'clearBtn': False,
                'endDate': "0d",
                'toggleActive': True,
                'autoclose': True,
            }
        ),
        help_text='Date when the claim was publicly stated, if known.',
    )
    context_description = forms.CharField(
        required=False,
        label='Context',
        max_length=300,
        help_text='Name of the event or description of the context of what was '
                  'said.',
    )
    context_url = forms.URLField(
        required=False,
        label='Link',
        max_length=300,
        help_text='If you can, please provide a link to the speech, press '
                  'release, video or other material that includes the claim.',
    )
    claim = forms.CharField(
        required=True,
        label='Claim',
        max_length=300,
        help_text='We prefer direct quotes. Otherwise, please accurately '
                  'paraphrase what was said.',
    )
    note = forms.CharField(
        required=False,
        label='Extra info',
        help_text='If you can, tell us more about how this was said and what it '
                  'means.',
        widget=forms.Textarea,
    )
    submitter_name = forms.CharField(
        required=False,
        label='Your name',
        help_text='First and last names, please.',
    )
    submitter_email = forms.EmailField(
        required=False,
        label='Your email',
        help_text='If you prefer we reach you by email.',
    )
    submitter_phone = PhoneNumberField(
        required=False,
        label='Your email',
        help_text='If you prefer we reach you by email.',
    )

    @property
    def submitter_field_names(self):
        """
        Return a tuple containing the list of ClaimSubmitter fields.
        """
        return (k for k in self.fields.keys() if "submitter_" in k)

    @property
    def has_submitter_data(self):
        """
        Return True of ClaimSubmitter data was submitted through the form.
        """

        if (
            bool(self.data['submitter_name']) or
            bool(self.data['submitter_phone']) or
            bool(self.data['submitter_email'])
        ):
            return True
        else:
            return False

    def clean(self):
        cleaned_data = super(ClaimForm, self).clean()

        if not bool(cleaned_data.get("source")):
            source = ClaimSource(
                source_type=cleaned_data.get("source_type"),
                name=cleaned_data.get("source_name"),
                title=cleaned_data.get("source_title"),
            )
            source.full_clean()

            cleaned_data['source'] = source

        if self.has_submitter_data:
            cleaned_data['submitter'] = self._submitter(
                cleaned_data.get("submitter_name"),
                cleaned_data.get("submitter_email"),
                cleaned_data.get("submitter_phone"),
            )
        else:
            cleaned_data['submitter'] = None

        return cleaned_data

    def _clean_submitter_data(self, name, email, phone):
        try:
            submitter = ClaimSubmitter.objects.get(
                name=name, email=email, phone=phone,
            )
        except ClaimSubmitter.DoesNotExist:
            submitter = ClaimSubmitter(
                name=name, email=email, phone=phone,
            )
            try:
                submitter.full_clean()
            except ValidationError as err:
                # TODO: override the field names 
                raise ValidationError

        return submitter
