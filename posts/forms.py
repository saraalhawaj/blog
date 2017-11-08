from django import forms
from .models import PostHome

class PostForm(forms.ModelForm):
	class Meta:
		model = PostHome
		fields = ['title','content']