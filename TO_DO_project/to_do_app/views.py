from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Task
from django.utils import timezone

# Create your views here.
from django.utils import timezone
from django.shortcuts import render
from to_do_app.models import Task

def task_list(request):
    # Base queryset for display
    task = Task.objects.all().order_by('-created_at')
    
    # Store original, unfiltered queryset for statistics
    all_tasks = Task.objects.all()
    
    # Get filter parameters
    search = request.GET.get('search', '')
    task_status = request.GET.get('task_status', '')
    due_today_param = request.GET.get('due_today', '')  # Add this
    
    # Search filter
    if search:
        task = task.filter(title__icontains=search)
    
    # Status filter - FIXED: Added due_today and overdue
    today = timezone.now().date()
    
    if task_status == 'completed':
        task = task.filter(completed=True)
    elif task_status == 'pending':
        task = task.filter(completed=False)
    elif task_status == 'overdue':
        task = task.filter(due_date__lt=today, completed=False)
    elif due_today_param == 'true' or task_status == 'due_today':
        task = task.filter(due_date=today, completed=False)
    
    # Statistics (from ALL tasks - these never change with filters)
    completed_task = all_tasks.filter(completed=True).count()
    pending_task = all_tasks.filter(completed=False).count()
    total_tasks = all_tasks.count()
    due_today = all_tasks.filter(due_date=today, completed=False).count()
    overdue = all_tasks.filter(due_date__lt=today, completed=False).count()
    
    context = {
        'task': task,
        'total_tasks': total_tasks,
        'completed_task': completed_task,
        'pending_task': pending_task,
        'due_today': due_today,
        'overdue': overdue,
        'search': search,
        'task_status': task_status,
        'due_today_param': due_today_param,
        'today': today,
    }
    
    return render(request, 'to_do_app/task_list.html', context)

def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        due_date = request.POST.get('due_date', '').strip() or None

        if title:
            Task.objects.create(
                title=title,
                description=description,
                due_date=due_date,
            )
            return redirect(reverse('to_do_app:task_list'))
        error = 'Title can not be Empty'
        return render(request, 'to_do_app/task_form.html', {'error': error})
    return render(request, 'to_do_app/task_form.html')

def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        completed = request.POST.get('completed') == 'on'
        due_date = request.POST.get('due_date', '').strip() or None

        if title:
            task.title = title
            task.description = description
            task.completed = completed
            task.due_date = due_date
            task.save()
            return redirect(reverse('to_do_app:task_list'))
        return render(request, 'to_do_app/task_form.html', {'task': task, 'error': 'Title can not be empty'})
    return render(request, 'to_do_app/task_form.html', {'task': task})

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect(reverse('to_do_app:task_list'))
    return render(request, 'to_do_app/task_confirm_delete.html', {'task': task})

def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.completed = not task.completed
        task.save()
        return redirect(reverse('to_do_app:task_list'))