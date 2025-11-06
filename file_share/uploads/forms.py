from django import forms
from .models import UploadedFile

# a form for uploading the files
class UploadForm(forms.ModelForm):
    expire_days = forms.IntegerField(
        required=False,
    )
    class Meta:
        model = UploadedFile
        fields = ['file','password','is_public','title','expire_days']



    def clean(self):
        cleaned_data = super(UploadForm, self).clean()
        is_public = cleaned_data.get('is_public')
        password = cleaned_data.get('password')
        if is_public is False and not password:
            self.add_error('password', 'password is required')
        if is_public:
            cleaned_data['password'] =''

        return cleaned_data