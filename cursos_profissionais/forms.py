from .models import Curso, Lead
from django import forms
from django.forms import ModelForm, ValidationError

class CursoForm(ModelForm):
    class Meta:
        model = Curso
        exclude = ['data_register']
        widgets = {
            'user_register': forms.HiddenInput(),       
        }

class LeadForm(ModelForm):
    
        class Meta:
            model = Lead
            exclude = ['data_register']
            widgets = {
                'curso': forms.HiddenInput(),
            }            