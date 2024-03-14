from django import forms 
from django.contrib.auth.models import User
from bookle.models import UserProfile
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.forms import UserCreationForm

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

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    user_picture = forms.ImageField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_picture')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Check if email is in the correct format
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Invalid email format.")

        # Check if email is unique
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already in use.")

        return email

    def clean_user_picture(self):
        user_picture = self.cleaned_data.get('user_picture')
        if not user_picture:
            raise ValidationError("You must upload a profile picture.")
        return user_picture

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(user=user, user_picture_file=self.cleaned_data['user_picture'])
        return user