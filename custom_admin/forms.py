from django import forms
from backend.models import Exam, Specialty

class DepartmentFilterForm(forms.Form):
    name = forms.CharField(required=False, label='Name')
    code = forms.CharField(required=False, label='Code')
    active = forms.ChoiceField(choices=[('', 'Any'), ('True', 'Yes'), ('False', 'No')], required=False, label='Active')

class GroupFilterForm(forms.Form):
    name = forms.CharField(required=False, label='Name')
    department = forms.CharField(required=False, label='Department')
    specialty = forms.CharField(required=False, label='Specialty')

class StudentFilterForm(forms.Form):
    full_name = forms.CharField(required=False, label='Full Name')
    student_id_number = forms.CharField(required=False, label='Student ID')
    department = forms.CharField(required=False, label='Department')

class StudentFilterForm(forms.Form):
    full_name = forms.CharField(required=False, label='Full Name')
    student_id_number = forms.CharField(required=False, label='Student ID')
    department = forms.CharField(required=False, label='Department')
    group = forms.CharField(required=False, label='Group')

class ExamForm(forms.ModelForm):
    oquv_reja = forms.ModelChoiceField(
        queryset=Specialty.objects.all(),
        label="O'quv reja",
        empty_label=None,
        to_field_name="name"  # Assuming Specialty has a name field
    )
    oquv_yili = forms.ChoiceField(
        choices=[("2024 (2024-2025)", "2024 (2024-2025)")],
        label="O'quv yili",
        disabled=True
    )
    semester = forms.ChoiceField(
        label="Semestr",
        required=False,
        choices=[]  # Will be populated dynamically
    )
    nazorat_turi = forms.ChoiceField(
        choices=[("Umumiy", "Umumiy"), ("Yakuniy nazorat", "Yakuniy nazorat")],
        label="Nazorat turi"
    )
    faol = forms.ChoiceField(
        choices=[(True, "Ha"), (False, "Yo'q")],
        label="Faol",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    boshlanish = forms.DateTimeField(
        label="Boshlanish",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    tugash = forms.DateTimeField(
        label="Tugash",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    vaqti_daqiqa = forms.IntegerField(
        label="Vaqti (daqiqa)",
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    maks_ball = forms.IntegerField(
        label="Maks. ball",
        min_value=1,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    urinishlar = forms.IntegerField(
        label="Urinishlar",
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    savollar_soni = forms.IntegerField(
        label="Savollar soni",
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    tasodifiy = forms.ChoiceField(
        choices=[(True, "Ha"), (False, "Yo'q")],
        label="Tasodifiy"
    )
    subject = forms.CharField(
        label="Fanlar",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Exam
        fields = ['name', 'description', 'oquv_reja', 'oquv_yili', 'semester', 'subject', 'nazorat_turi', 
                  'faol', 'boshlanish', 'tugash', 'vaqti_daqiqa', 'maks_ball', 'urinishlar', 
                  'savollar_soni', 'tasodifiy']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set semester choices based on oquv_reja
        if self.instance and self.instance.oquv_reja:
            year_part = self.instance.oquv_reja.name.split('(')[1].split('-')[0]  # Extract year like "2021"
            if int(year_part) == 2021:
                self.fields['semester'].choices = [('7-semestr', '7-semestr'), ('8-semestr', '8-semestr')]
            elif int(year_part) == 2022:
                self.fields['semester'].choices = [('5-semestr', '5-semestr'), ('6-semestr', '6-semestr')]
            else:
                self.fields['semester'].choices = []
        else:
            self.fields['semester'].choices = []

        # Make all fields read-only if the exam is saved and faol is True
        if self.instance.pk and self.instance.faol:
            for field in self.fields:
                if field != 'faol':
                    self.fields[field].widget.attrs['readonly'] = True