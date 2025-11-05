from django import forms
from .models import UploadedFile


class UploadForm(forms.ModelForm):

    class Meta:
        model = UploadedFile
        fields = ['file','password','is_public','title']


    def clean(self):
        cleaned_data = super(UploadForm, self).clean()
        is_public = cleaned_data.get('is_public')
        password = cleaned_data.get('password')
        if is_public is False and not password:
            self.add_error('password', 'password is required')
        if is_public:
            cleaned_data['password'] =''

        return cleaned_data