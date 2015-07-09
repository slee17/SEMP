from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _ # For enabling translation.

from .models import Shift

# Form for creating a shift.
class ShiftAdminForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['owner', 'day_of_the_week', 'department', 'location', 'start_date', 'end_date',
                  'start_time', 'end_time', 'activated']

    def clean(self):
        cleaned = self.cleaned_data
        
        start_time = cleaned.get('start_time')
        end_time = cleaned.get('end_time')
        start_date = cleaned.get('start_date')
        end_date = cleaned.get('end_date')

        if end_time < start_time:
            time_error_message = "End time should be after start time."
            self.add_error('end_time', time_error_message)

        if end_date < start_date:
            date_error_message = "End date should be after start date."
            # self.add_error('start_date', date_error_message)
            self.add_error('end_date', date_error_message)
            # date_error = forms.ValidationError(_('Start date should be before end date.'), code='invalid_date')
            
        return self.cleaned_data