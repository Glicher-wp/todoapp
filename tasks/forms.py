from django import forms

from .models import TodoItem


class AddTasksForm(forms.Form):
    description = forms.CharField(max_length=64, label='')


class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ("description", "priority", "tags")
        labels = {"description": "Описание", "priority": "", "tags": "тэги"}


class TodoItemExportForm(forms.Form):
    prio_high = forms.BooleanField(
        label="Высокая важность", initial=True, required=False,
    )
    prio_med = forms.BooleanField(
        label="средней важности", initial=True, required=False,
    )
    prio_low = forms.BooleanField(
        label="низкой важности", initial=False, required=False,
    )
