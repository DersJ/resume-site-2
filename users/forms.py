from django import forms
from .models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UpdateUserForm(forms.ModelForm):
    full_name = forms.CharField(max_length=128, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    display_name = forms.CharField(max_length=64, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name which other users will see (required)'}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell about yourself! (optional)'}))
    subscribe_email_updates = forms.BooleanField(widget=forms.CheckboxInput,required=False, label='Subscribe to email updates for new posts')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'profile-form'
        self.helper.add_input(Submit('submit', 'Save', css_class='bg-primary text-dark mt-2 form-submit'))


    class Meta: 
        model = User
        fields = ['display_name', 'full_name', 'bio', 'subscribe_email_updates']