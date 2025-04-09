from django import forms
from .models import FoodEntry

class FoodEntryForm(forms.ModelForm):
    class Meta:
        model = FoodEntry
        fields = ['dishes', 'waste_reason', 'comments']
        widgets = {
            'dishes': forms.CheckboxSelectMultiple(),
            'waste_reason': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Explain why you wasted food (if applicable)'
            }),
            'comments': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Any additional comments?'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        waste_reason = cleaned_data.get('waste_reason')

        if waste_reason and len(waste_reason.strip()) < 5:
            self.add_error('waste_reason', 'Please add more detail to your reason.')

        return cleaned_data
