from django import forms
from .models import Comment, Post
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = [
			"title",
			"content",
			"image",
			"public",
			"isMarkdownContent",
		]

class CommentForm(forms.ModelForm):
	content = forms.CharField(label='', widget=forms.Textarea(attrs={
		'class': 'form-control', 
		'placeholder': 'Comment', 
		'rows': '4', 
		'cols': '50', 
		'required': True, 
		'maxlength': '1500',
		'onkeyup': 'countChars(this)'
	}))

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_class = 'comment-form'
		self.helper.form_action = 'submit_survey'

		self.helper = FormHelper()
		self.helper.add_input(Submit('submit', 'Submit', css_class="bg-primary"))

	class Meta:
		model = Comment
		fields = [
			"content",
		]

	 