from django.forms.models import ModelForm
from project.models import Project
from django.forms.widgets import TextInput
from django.forms.fields import CharField

class ChangeTitleForm(ModelForm):
    title = CharField(
        label='',
        widget=TextInput(attrs={
            'class' : 'projectTitle',
        }),
    )
    
    class Meta:
        model = Project
        fields=('title',)
