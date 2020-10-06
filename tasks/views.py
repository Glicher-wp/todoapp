from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import TodoItem
from .forms import TodoItemForm, TodoItemExportForm, ImportTaskForm
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from taggit.models import Tag
from trello import TrelloClient

class TaskListView(LoginRequiredMixin, ListView):
    model = TodoItem
    context_object_name = "tasks"
    template_name = "tasks/list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        u = self.request.user
        return qs.filter(owner=u)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_tasks = self.get_queryset()
        tags = []
        for t in user_tasks:
            tags.append(list(t.tags.all()))
            
        context['tags'] = filter_tags(tags)
        return context


class TaskListUncompleted(TaskListView):
    template_name = "tasks/uncompleted_list.html"


class TaskListGrouped(TaskListView):
    template_name = "tasks/grouped_tasks.html"


class TaskCreateView(View):
    def my_render(self, request, form):
        return render(request, "tasks/create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = TodoItemForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            form.save_m2m()
            messages.success(request, "Задача была успешно создана")
            return redirect(reverse("tasks:list"))

        return self.my_render(request, form)

    def get(self, request, *args, **kwargs):
        form = TodoItemForm()
        return self.my_render(request, form)


class TaskDetailsView(DetailView):
    model = TodoItem
    template_name = 'tasks/details.html'
    # delta = TodoItem.delta_time - timedelta(TodoItem.created)
    # extra_context = {"time": delta}


class TaskEditView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        t = TodoItem.objects.get(id=pk)
        form = TodoItemForm(request.POST, instance=t)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            messages.success(request, "Задача успешно изменена")
            return redirect(reverse("tasks:list"))
        else:
            messages.error(request, "Что-то пошло не так, попробуйте снова")

        return render(request, "tasks/edit.html", {"form": form, "task": t})

    def get(self, request, pk, *args, **kwargs):
        t = TodoItem.objects.get(id=pk)
        form = TodoItemForm(instance=t)
        return render(request, "tasks/edit.html", {"form": form, "task": t})


class TaskImportView(View):

    def my_render(self, request, form):
        return render(request, "tasks/import.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = ImportTaskForm(request.POST)
        key = request.user.profile.key
        secret = request.user.profile.token
        if key and secret:
            client = TrelloClient(key, secret)
        if form.is_valid():
            form = form['board_id'].value()
            u = request.user
            tasks = TodoItem.objects.filter(owner=u).all()
            tasks.delete()
            new_tasks = tasks_import(client, form)
            for task in new_tasks:
                created_task = TodoItem(owner=u, description=task.name, TRELLO_ID=task.id).save()

            messages.success(request, "Задачи были успешно импортированны")
            return redirect(reverse("tasks:list"))

        return self.my_render(request, form)

    def get(self, request, *args, **kwargs):
        form = ImportTaskForm()
        return self.my_render(request, form)


class TaskExportView(LoginRequiredMixin, View):
    def generate_body(self, user, priorities):
        q = Q()
        if priorities["prio_high"]:
            q = q | Q(priority=TodoItem.PRIORITY_HIGH)
        if priorities["prio_med"]:
            q = q | Q(priority=TodoItem.PRIORITY_MEDIUM)
        if priorities["prio_low"]:
            q = q | Q(priority=TodoItem.PRIORITY_LOW)
        tasks = TodoItem.objects.filter(owner=user).filter(q).all()

        body = "Ваши задачи и приоритеты: \n"
        for t in list(tasks):
            if t.is_completed:
                body += f"[x] {t.description} ({t.get_priority_display()})\n"
            else:
                body += f"[] {t.description} ({t.get_priority_display()})\n"
        return body

    def post(self, request, *args, **kwargs):
        form = TodoItemExportForm(request.POST)
        if form.is_valid():
            email = request.user.email
            body = self.generate_body(request.user, form.cleaned_data)
            send_mail("Задачи", body, settings.EMAIL_HOST_USER, [email])
            messages.success(request, "Задачи были отправлены на почту %s % email")
        else:
            messages.error(request, "Что-то пошло не так, попробуйте еще раз")
        return redirect(reverse("tasks:list"))

    def get(self, request, *args, **kwargs):
        form = TodoItemExportForm()
        return render(request, "tasks/export.html", {"form": form})


@login_required
def index(request):
    return HttpResponse("Примитивный ответ из приложения tasks")


def complete_task(request, uid):
    t = TodoItem.objects.get(id=uid)
    t.is_completed = True
    t.save()
    if t.TRELLO_ID:
        key = request.user.profile.key
        secret = request.user.profile.token
        client = TrelloClient(key, secret)
        card = client.get_card(t.TRELLO_ID)
        board_id = card.board_id
        board = client.get_board(board_id)
        card.change_list(board.list_lists()[-1].id)
    messages.success(request, "Задача выполнена")
    return HttpResponse("OK")


def delete_task(request, uid, tag_slug=None):
    t = TodoItem.objects.get(id=uid)
    t.delete()
    messages.success(request, "Задача удалена")
    if tag_slug:
        return redirect(reverse("tasks:list_by_tag", kwargs={"tag_slug": tag_slug}))
    else:
        return redirect(reverse("tasks:list"))


def filter_tags(tags):
    tasks_tags = []
    for tag in tags:
        for i in tag:
            if i not in tasks_tags:
                tasks_tags.append(i)
    return tasks_tags


def tasks_by_tag(request, tag_slug=None):
    u = request.user
    tasks = TodoItem.objects.filter(owner=u).all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        tasks = tasks.filter(tags__in=[tag])

    all_tags = []
    for t in tasks:
        all_tags.append(list(t.tags.all()))
    all_tags = filter_tags(all_tags)

    task_counter = len(tasks)

    return render(
        request,
        "tasks/list_by_tag.html",
        {"tag": tag, "tasks": tasks, "all_tags": all_tags, "task_counter": task_counter},
        )


def tasks_import(client, board_id):
    """
    :param key: Trello key
    :param secret: Trello secret token
    :param board_id: id board from which user want's to import tasks
    :return: list of Trello cards from the selected board
    """
    board = client.get_board(str(board_id))
    to_do = board.list_lists()[0]
    tasks = to_do.list_cards()
    return tasks


def zero_devision_test(request):
    1/0
