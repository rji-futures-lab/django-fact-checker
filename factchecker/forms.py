from bootstrap_datepicker.widgets import DatePicker
from django import forms
from .models import ClaimSource, Claim


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
    extra = forms.CharField(
        required=False,
        label='Extra info',
        help_text='If you can, tell us more about how this was said and what it '
                  'means, if you can.',
        widget=forms.Textarea,
    )

    def clean(self):
        cleaned_data = super().clean()

        has_source_selected = bool(self.cleaned_data.get("source"))
        has_source_type = bool(self.cleaned_data.get("source_type"))
        has_source_name = bool(self.cleaned_data.get("source_name"))
        
        print(self.errors.as_data())
        
        if not has_source_selected:
            msg = "This field is required when adding a new source."

            if not has_source_type:
                self.add_error("source_type", msg)
                
            if not has_source_name:
                self.add_error("source_name", msg)
            
            del self.errors['source']

        print(self.errors.as_data())
