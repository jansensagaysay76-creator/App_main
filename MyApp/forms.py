from django import forms

from .models import Pet


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            "name",
            "pet_type",
            "breed",
            "age",
            "gender",
            "owner_name",
            "contact_number",
        ]
        widgets = {
            "age": forms.NumberInput(attrs={"min": 0}),
        }
