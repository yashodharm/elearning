from django import forms
from .models import *
import re
# from tinymce.widgets import TinyMCE

class AddWebinarForm(forms.ModelForm):
    class Meta:
        model = Webinar
        fields = ['webinar_name', 'for_everybody','text','link']

    def clean_webinar_name(self):
        webinar_name = self.cleaned_data.get('webinar_name')

        regexp = re.compile(r'[0-9a-zA-Z ]')
        if not regexp.match(webinar_name):
            raise forms.ValidationError("Please make sure webinar name contains (a-z, A-Z, 0-9, space) characters")

        return webinar_name


class AddSessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['session_name']

    def clean_session_name(self):
        session_name = self.cleaned_data.get('session_name')
        regexp = re.compile(r'[0-9a-zA-Z ]')

        if not regexp.match(session_name):
            raise forms.ValidationError("Please make sure session name contains (a-z, A-Z, 0-9, space) characters")

        return session_name


class AddLinkForm(forms.ModelForm):
    class Meta:
        model = YTLinkW
        fields = ['link']


class AddTxtForm(forms.ModelForm):

    # lesson = forms.CharField(widget=TinyMCE())
    class Meta:
        model = TextBlockW
        fields = ['lesson']

class AddGDLinkForm(forms.ModelForm):
    class Meta:
        model = gdlinkW
        fields = ['link']




class EditWebinarForm(forms.ModelForm):
    class Meta:
        model = Webinar
        fields = ['webinar_name', 'for_everybody','text','link']


class EditSessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['session_name']


class EditYTLinkForm(forms.ModelForm):
    class Meta:
        model = YTLinkW
        fields = ['link']

class EditGDLinkForm(forms.ModelForm):
    class Meta:
        model = gdlinkW
        fields = ['link']

class EditTxtForm(forms.ModelForm):
    class Meta:
        model = TextBlockW
        fields = ["lesson"]


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUploadW
        fields = ['file']
