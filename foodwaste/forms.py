from django import forms
from .models import FoodEntry

class FoodEntryForm(forms.ModelForm):
    class Meta:
        model = FoodEntry
        fields = ['dish', 'liked', 'eaten_amount', 'waste_amount', 'waste_reason', 'rating', 'comments']
        widgets = {
            'waste_reason': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Explain why you wasted food (if applicable)'}),
            'comments': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any additional comments?'}),
            'rating': forms.Select(choices=[(i, '⭐' * i) for i in range(1, 6)]),
        }

    def clean(self):
        cleaned_data = super().clean()
        waste_amount = cleaned_data.get('waste_amount')
        waste_reason = cleaned_data.get('waste_reason')

        if waste_amount in ['Some', 'Lot'] and not waste_reason:
            self.add_error('waste_reason', 'Please provide a reason for wasting food.')
        
        return cleaned_data
