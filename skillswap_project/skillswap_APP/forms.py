from django import forms
from .models import Profile, SkillSwapRequest

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location', 'skills_offered', 'skills_wanted', 'availability', 'visibility', 'profile_pic']
        widgets = {
            'skills_offered': forms.TextInput(attrs={'placeholder': 'e.g. Java, Python, Web Design'}),
            'skills_wanted': forms.TextInput(attrs={'placeholder': 'e.g. Flutter, Video Editing'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Ahmedabad'}),
        }

class SkillSwapRequestForm(forms.ModelForm):
    class Meta:
        model = SkillSwapRequest
        fields = ['offered_skill', 'requested_skill', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write a message to the recipient (optional)...'}),
            'offered_skill': forms.TextInput(attrs={'placeholder': 'e.g. Python'}),
            'requested_skill': forms.TextInput(attrs={'placeholder': 'e.g. UI/UX Design'}),
        }
