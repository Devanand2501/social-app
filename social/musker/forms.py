from django import forms 
from .models import Tweet

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
        exclude=("user",)