from django import forms
from .models import STATUS_CHOICES,TYPES_CHOICES

default_status = STATUS_CHOICES[0][0]
default_type = TYPES_CHOICES[0][0]
BROWSER_DATETIME_FORMAT = '%Y-%m-%dT%H:%M'

class ArticleForm(forms.Form):
    description = forms.CharField(max_length=200, required=True, label='Описание')
    maxdescription = forms.CharField(max_length=3000, required=True, label='Подробное описание', widget=forms.Textarea)
    status = forms.ChoiceField(choices=STATUS_CHOICES, initial=default_status, label='Статус')
    type = forms.ChoiceField(choices=TYPES_CHOICES, initial=default_type, label='Тип')
    publish_at = forms.DateTimeField(required=False, label='Время публикации',
                                     input_formats=['%Y-%m-%d', BROWSER_DATETIME_FORMAT,
                                                    '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M',
                                                    '%Y-%m-%d %H:%M:%S'],
                                     widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
