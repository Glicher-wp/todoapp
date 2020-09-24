from django import forms

from .models import TodoItem


class AddTasksForm(forms.Form):
    description = forms.CharField(max_length=64, label='')


class ImportTaskForm(forms.ModelForm):
    """

    create form for importing tasks from trello.com

    """
    class Meta:
        model = TodoItem
        fields = ("board_id", )
        labels = {"board_id": "id доски"}


class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ("description", "priority", "tags", "TRELLO_ID")
        labels = {"description": "Описание", "priority": "", "tags": "тэги", "TRELLO_ID": "id задачи"}


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
