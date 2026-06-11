from django.shortcuts import render, get_object_or_404, redirect
from .froms import StudentsForm
from .models import Students

# Create your views here.

def student_create(request):
    form = StudentsForm()
    if request.method == 'POST':
        form = StudentsForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'students/student_success.html')
    return render(request, 'students/student_form.html', {'form':form})

def student_list(request):
    students = Students.objects.all()
    return render(request, 'students/student_list.html', {'students':students})

def student_details(request, pk):
    student = get_object_or_404(Students, pk=pk)
    return render(request, 'students/student_details.html', {'student':student})

def student_edit(request, pk):
    student = get_object_or_404(Students, pk=pk)
    if request.method == 'POST':
        form = StudentsForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentsForm(instance=student)
    return render(request, 'students/student_form.html', {'form':form})

def student_delete(request, pk):
    student = get_object_or_404(Students, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student':student})