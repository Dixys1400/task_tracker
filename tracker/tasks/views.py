from .models import Task
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import TaskSerializer
from rest_framework import viewsets
from .forms import TaskForm
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework import status
import random

# API (DRF)
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(summary='Get percent of task', description='Percent of Task', responses={200, TaskSerializer})
    @action(detail=False, methods=['get'])
    def percent_progress(self, request, permission_classes=[]):
        total = Task.objects.count()
        done = Task.objects.filter(status='done').count()
        percent = 0 if total == 0 else (done / total) * 100
        return Response({
            'percent_progress': round(percent, 2)
        })

    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None, permission_classes=[]):
        task = self.get_object()
        task.status = 'done'
        task.save()
        return Response({'status': 'task marked as complete'})

    @action(detail=False, methods=['get'])
    def motivation(self, request):
        user_tasks = Task.objects.filter(user=request.user)
        total = user_tasks.count()
        done = user_tasks.filter(status="done").count()
        left = total - done

        if total == 0:
            message = "У тебя пока нет задач. Добавь первую"
        elif left == 0:
            message = "Все задачи выполнены"
        elif left <= 2:
            message = f"Осталось всего {left} задач"
        else:
            phrases = [
                f"У тебя ещё {left} задач(и), но ты справишься",
                "Не сдавайся, каждый шаг приближает к цели!",
                "Ты делаешь больше, чем думаешь",
                "Работай тихо — пусть результат делает шум",
                "Тише едешь — дальше будешь. Главное — не останавливаться",
                "Каждая выполненная задача — это кирпич в стене твоего успеха"
            ]
            message = random.choice(phrases)

        return Response(
            {"motivation": message, "done": done, "left": left, "total": total},
            status=status.HTTP_200_OK
        )


# Django Templates
# @cache_page(60)
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_detail", pk=task.pk)
    else:
        form = TaskForm(instance=task)

    return render(request, "task_detail.html", {"task": task, "form": form})



def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'task_form.html', {'form': form})


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')

    else:
        form = TaskForm(instance=task)

    return render(request, 'task_edit.html', {'form': form, 'task': task})



def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("task_list")
    return redirect("task_detail", pk=pk)

