from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _ # Enable translation.

from .models import Shift, Sale

# Form for creating shifts and validating fields.
class ShiftAdminForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['owner', 'department', 'location', 'start_date', 'recurrences',
                  'start_time', 'end_time', 'spans_past_midnight', 'activated']

    def clean(self):
        cleaned = self.cleaned_data
        
        start_time = cleaned.get('start_time')
        end_time = cleaned.get('end_time')
        # start_date = cleaned.get('start_date')
        # end_date = cleaned.get('end_date')

        spans_past_midnight = cleaned.get('spans_past_midnight')

        error = False
        error_field = []
        error_message = []

        if end_time < start_time:
            error = True
            error_field.append("end_time")
            error_message.append("End time should be after start time. "
                        "If the shift spans over midnight, check the 'Spans over midnight' box.")
            if spans_past_midnight == True:
                error_field.remove("end_time")
                error_message.remove("End time should be after start time. "
                        "If the shift spans over midnight, check the 'Spans over midnight' box.")

        # if end_date < start_date:
        #    error = True
        #    error_field.append("end_date")
        #    error_message.append("End date should be after start date.")

        if error:
            for i in range(len(error_field)):
                self.add_error(error_field[i], error_message[i])
            
        return self.cleaned_data

class CreateSale(ModelForm):
    reason = forms.CharField(initial=u'Explain your reason for selling this shift.', label='')

    class Meta:
        model = Sale # Create form based off the Sale model.
        fields = ['shift', 'date', 'seller', 'buyer']

    # def clean(self): # Necessary?
    #    return self.cleaned_data

    # def clean_sale_form(self):
    #    cleaned_reason = self.cleaned_data.get('reason')
    #    return cleaned_reason

"""
class ShiftSaleForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['sale_status']
        widgets = {
            'sale_status': forms.CheckboxInput(
                attrs={'id': 'shift-sale', 'required': True}
            ),
        }
"""