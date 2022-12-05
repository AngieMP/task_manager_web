from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect

from . import models
from . import forms

def homepage(request):
    fecha = timezone.now().date()
    tareas = (
        models.Task.objects
        .all()
        .filter(finished=False)
        .select_related('project')
    )
    
    return render(request, 'tasks/homepage.html', {
        'fecha': fecha,
        'tareas': tareas 
    }) 

def lista_proyectos(request):
    projects = models.Project.objects.all()
    return render(request, 'tasks/projects.html', {
        'projects': projects,
    })
    
def tareas_urgentes(request):
    tareas = (
        models.Task.objects
        .all()
        .filter(priority='H')
        # .filter(finished=False)
        .filter(project__isnull=True)
        .order_by('orden', 'name')
    )
    
    return render(request, 'tasks/tareas_urgentes.html', {
        'tareas': tareas 
    })
    
def tareas_no_urgentes(request):
    tareas = (
        models.Task.objects
        .all()
        .filter(priority='L')
        # .filter(finished=False)
        # .filter(orden__lt=200)
        .filter(project__isnull=True)
        .order_by('orden', 'name')
    )
    
    return render(request, 'tasks/tareas_no_urgentes.html', {
        'tareas': tareas 
    }) 
    
def detalle_proyecto(request, pk):
    project = models.Project.objects.get(pk=pk)
    return render(request, 'tasks/detalle_proyecto.html', {
        'project': project,
    })
    
def buscar_tareas(request):
    tareas = []
    num_tareas = 0
    if request.method == 'POST':
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            priority = form.cleaned_data['priority']
            # import logging
            # logging.warning(f"{priority=}") para ver en django debug toolbar
            tareas = models.Task.objects.filter(name__icontains=query)
            if priority:
                tareas = tareas.filter(priority__in=priority) # pongo esto para que haga un "or" en vez de un "and"
            num_tareas = tareas.count()
    else:
        form = forms.SearchForm()
    return render(request, 'tasks/buscar_tareas.html', {
        'form': form,
        'tareas': tareas,
        'num_tareas': num_tareas,
    
    })

def crear_proyecto(request):
    if request.method == 'POST':
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/projects/')
    else:
        form = forms.ProjectForm()
    return render(request, 'tasks/crear_proyecto.html', {
        'form': form
        })
    
def detalle_proyecto_code(request, code):
    project = models.Project.objects.get(code=code)
    tareas = project.task_set.all()
    return render(request, 'tasks/detalle_proyecto.html', {
        'project': project,
        'tareas': tareas,
    })
    
def crear_tareas(request):
    if request.method =='POST':
        form = forms.MultipleTasksForm(request.POST)
        if form.is_valid():
            newtasks = form.cleaned_data['newtasks']
            for task in newtasks.split("\n"):
                models.Task(name=task).save() # Creo un objeto tarea solo con el nombre
            return redirect('/createtasks')
    else:
        form = forms.MultipleTasksForm()
    return render(request, 'tasks/crear_tareas.html', {'form' : form})
