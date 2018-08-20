from django import forms
from django.utils.translation import ugettext_lazy as _

from tracker.models import Event
from tracker.widgets import ColorInput


class SpanForm(forms.ModelForm):
    start = forms.SplitDateTimeField(label=_("start"))
    end = forms.SplitDateTimeField(label=_("end"),
                                   help_text=_("The end time muse be later than start time."))
    
    def clean(self):
        if 'end' in self.cleaned_data and 'start' in self.cleaned_data:
            if self.cleaned_data['end'] <= self.cleaned_data['start']:
                raise forms.ValidationError(_("The end time must be later than start time."))
        return self.cleaned_data


class EventForm(SpanForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
    

    class Meta:
        model = Event
        exclude = ('creator', 'created_on', )


class EventAdminForm(forms.ModelForm):
    class Meta:
        exclude = []
        model = Event
        widgets = {
            'color_event': ColorInput
        }