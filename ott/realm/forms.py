from django import forms

class SignInForm(forms.Form):
    mobile_number = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=150)
    mobile_number = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)



from django import forms
from .models import Video,Genres

class VideoUploadForm(forms.ModelForm):
    genres = forms.ModelChoiceField(queryset=Genres.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Video
        fields = ('title', 'description', 'video_file', 'thumbnail', 'scheduled_time', 'category', 'genres', 'content_age_rating')
        
        
        
