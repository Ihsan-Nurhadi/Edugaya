from django import forms
from .models import Post , Class
from learning_style.models import LearningCharacteristic

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'video', 'thumbnail', 'price','learning_style')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'video': forms.URLInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'learning_style': forms.Select(attrs={'class': 'form-control'}),
        }
class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ('post', 'class_name', 'text', 'video')  # Tambahkan 'post'
        widgets = {
            'class_name': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'video': forms.URLInput(attrs={'class': 'form-control'}),
            'post': forms.Select(attrs={'class': 'form-control'}),  # Styling select input
        }

    def __init__(self, *args, **kwargs):
        # Ambil user dari kwargs dan hapus agar tidak ada error
        user = kwargs.pop('user', None)
        super(ClassForm, self).__init__(*args, **kwargs)
        
        # Filter queryset untuk field 'post' agar hanya mencakup postingan milik user (guru)
        if user is not None:
            self.fields['post'].queryset = Post.objects.filter(author=user)


class LearningCharacteristicForm(forms.ModelForm):
    class Meta:
        model = LearningCharacteristic
        fields = ('code', 'question', 'category', 'probability')
        widgets ={
            'code': forms.TextInput(attrs={'class':'form-control'}),
            'question': forms.TextInput(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'probability': forms.NumberInput(attrs={'class':'form-control'}),
        }

