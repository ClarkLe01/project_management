from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Project

widgets_general = {
    'name': forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg form-control-solid',
            'placeholder': 'Your Name Project',
        }
    ),
}


class ProjectForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Project
        fields = '__all__'
