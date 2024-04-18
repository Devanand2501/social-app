from typing import Any
from django import forms 
from .models import Tweet,Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Profile Picture")
    profile_bio = forms.CharField(label="Profile Bio", required=False,widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'Profile Bio'
    }))
    portfolio_link = forms.CharField(label="",max_length=100, required=False,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Portfolio Link'
    }))
    facebook_link = forms.CharField(label="",max_length=100, required=False,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Facebook Link'
    }))
    instagram_link = forms.CharField(label="",max_length=100, required=False,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Instagram Link'
    }))
    twitter_link = forms.CharField(label="",max_length=100, required=False,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Twitter Link'
    }))
    linkedin_link = forms.CharField(label="",max_length=100, required=False,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Linkedin Link'
    }))
    class Meta:
        model = Profile
        fields = ('profile_image','profile_bio','portfolio_link','facebook_link','instagram_link','twitter_link','linkedin_link')
class TweetForm(forms.ModelForm):
    body = forms.CharField(required=True,
            widget=forms.widgets.Textarea(
                attrs={
                    "class":"form-control",
                    "placeholder":"Write your tweets"
                }
            ),
            label="",
            )
            
    class Meta:
        model = Tweet
        exclude=("user","likes")

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", required=True,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter your email'
    }))
    first_name = forms.CharField(label="",max_length=100, required=True,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter your first name'
    }))
    last_name = forms.CharField(label="",max_length=100, required=True,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter your last name'
    }))

    class Meta:
        model = User
        fields = ("username","email","first_name","last_name","password1","password2")
    
    def __init__(self, *args: Any, **kwargs: Any):
        super(SignUpForm,self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        # self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        # self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        # self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

    def clean(self):
        cleaned_data = super().clean()
        # username = cleaned_data['username']
        username = cleaned_data.get('username')
        print(f"Username : {username}")

        if username.isalpha() != True and  username.isnumeric() == True:
            # raise ValidationError("Username must contain characters also!")
            self.add_error("username","Username must contain characters also!")

        if username.isnumeric() != True and username.isalpha() == True:
            # raise ValidationError("Username must contain numbers!")
            self.add_error("username","Username must contain numbers also!")

        if username.isalnum() == True :
            # raise ValidationError("Username must contain characters!")
            pass