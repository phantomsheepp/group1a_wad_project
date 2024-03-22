from django import forms 
from django.contrib.auth.models import User
from bookle.models import Score, UserProfile
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.forms import UserCreationForm
from django import forms
from bookle.models import Comment

# Is this used anywhere?
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
class ProfileEditForm(forms.ModelForm):
    bio = forms.CharField(required=False)
    user_picture = forms.ImageField(required=False)
    
    class Meta:
        model = UserProfile
        fields = ('bio', 'user_picture')

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    bio = forms.CharField(required=False)
    user_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_picture')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Invalid email format.")

        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already in use.")

        return email

    def clean_user_picture(self):
        user_picture = self.cleaned_data.get('user_picture')
        return user_picture

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.puzzle = kwargs.pop('puzzle', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.userID = self.user
        comment.puzzleID = self.puzzle
        if commit:
            comment.save()
        return comment
    
class ScoreForm(forms.ModelForm):
    difficulty = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)])
    popularity = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)])

    class Meta:
        model = Score
        fields = ['difficulty', 'popularity']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.puzzle = kwargs.pop('puzzle', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        score = super().save(commit=False)
        score.userID = self.user
        score.puzzleID = self.puzzle
        if commit:
            score.save()
        return score