from django import forms 
from django.contrib.auth.models import User
from bookle.models import UserProfile
from django.core.exceptions import ValidationError

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
class UserProfileForm(forms.ModelForm):
    user_picture = forms.ImageField()
    
    class Meta:
        model = UserProfile
        exclude = ('user','bio','user_picture_file')

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Password confirmation')
    user_picture = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError("Passwords must match")

    def save(self):
        cleaned_data = self.cleaned_data
        user = User.objects.create_user(
            username=cleaned_data.get("username"),
            email=cleaned_data.get("email"),
            password=cleaned_data.get("password1")
        )
        user_profile = UserProfile.objects.create(
            user=user,
            user_picture_file=cleaned_data.get("user_picture")
        )
        return user