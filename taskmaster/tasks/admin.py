from django.contrib import admin

from . import models

class TaskAdmin(admin.ModelAdmin):
    date_hierarchy = "due_date"
    search_fields = ['name, due_date']
    list_filter = ['priority', 'due_date', 'finished']
    list_display = [
        'name',
        'priority',
        'due_date',
        'orden',
        'is_due',
        'matraca'
    ]

    @admin.display(boolean=True)
    def matraca(self, instance):
        return instance.name.lower().startswith('a')
    
admin.site.register(models.Task, TaskAdmin)

class ProjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Project, ProjectAdmin)
