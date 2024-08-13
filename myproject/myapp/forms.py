from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import MyUser

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('phone_number', 'name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = MyUser.objects.generate_username(self.cleaned_data['name'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    phone_number = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'time', 'num_of_people', 'special_requests']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'HH:MM'}),
            'num_of_people': forms.NumberInput(attrs={'min': 1}),
            'special_requests': forms.Textarea(attrs={'placeholder': 'Any special requests'}),
        }
        help_texts = {
            'date': 'Please enter a valid date in YYYY-MM-DD format.',
            'time': 'Please enter a valid time in HH:MM format.',
        }



from django import forms
from .models import MenuItem, Category

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['category', 'name', 'price', 'size', 'special', 'image']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
