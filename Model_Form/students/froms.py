from django import forms
from .models import Students

class StudentsForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['name', 'age', 'email']

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            raise forms.ValidationError("Age must be at least 18.")
        return age