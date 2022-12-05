from django import forms
from . import models

class SearchForm(forms.Form):
    query = forms.CharField(label="buscar")
    priority = forms.MultipleChoiceField(
        label='Prioridad',
        choices=[
            ('H', 'Alta'),
            ('N', 'Normal'),
            ('L', 'Baja'),       
            
        ],
        widget  = forms.CheckboxSelectMultiple(), # le digo el control que quiero que use 
        initial = ['H', 'N'], # que esté esto marcado por defecto
        required = False, # no voy a exigir que me marque una prioridad 
    )
    
class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'name',
            'code',
            'description',
            'start_date',
            'end_date',
        ]
        
class MultipleTasksForm(forms.Form):
    newtasks = forms.CharField(
        label= 'Mis nuevas tareas',
        widget=forms.Textarea(), # En Textinput solo me cabe una linea
        )