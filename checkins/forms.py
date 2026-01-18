from django import forms
from .models import CheckIn

class CheckInForm(forms.ModelForm):
    class Meta:
        model = CheckIn
        fields = ['date', 'weight_lb', 'bodyfat_percent', 'muscle_lb', 'waist_in','chest_in', 'hips_in', 'biceps_in', 'thigh_in', 'calf_in', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'weight_lb': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'bodyfat_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'muscle_lb': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'waist_in': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
	    'chest_in': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
	    'hips_in': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
	    'biceps_in': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
	    'thigh_in': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
	    'calf_in': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
