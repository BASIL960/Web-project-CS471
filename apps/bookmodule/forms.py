from django import forms
from .models import Student, Student2

# Task 1: استمارة الطالب (One-to-Many)
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'address']
        widgets = {
            'address': forms.Select(attrs={'class': 'form-control'}), # قائمة منسدلة
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Task 2: استمارة الطالب 2 (Many-to-Many)
class Student2Form(forms.ModelForm):
    class Meta:
        model = Student2
        fields = ['name', 'age', 'addresses']
        widgets = {
            'addresses': forms.CheckboxSelectMultiple(), # مربعات اختيار متعددة
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# تأكد من استيراد النموذج الجديد
from .models import StudentImage

# أضف هذا الكلاس
class StudentImageForm(forms.ModelForm):
    class Meta:
        model = StudentImage
        fields = ['title', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            # ImageField لا يحتاج widget خاص عادةً، جانجو يتكفل به
        }