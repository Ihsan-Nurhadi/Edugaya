from django import forms
from .models import LearningCharacteristic
from .models import Student

class LearningStyleForm(forms.Form):
    # Menggunakan ModelChoiceField untuk mengambil nama murid
    student = forms.ModelChoiceField(queryset=Student.objects.all(), empty_label="Pilih Nama Murid", to_field_name='name')  # Pilih nama murid dari field 'name'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pilih ciri-ciri dari LearningCharacteristic
        choices = [(char.id, f"{char.code}. {char.question}") for char in LearningCharacteristic.objects.all()]
        self.fields['selected'] = forms.MultipleChoiceField(
            choices=choices,
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            label="Ciri-Ciri Yang Dipilih (Minimal 3)"
        )

    def clean_selected(self):
        selected = self.cleaned_data.get('selected')
        if len(selected) < 3:
            raise forms.ValidationError("Pilih minimal 3 ciri-ciri.")
        return selected



# class StudentForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ['name']
