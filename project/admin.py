from django.contrib import admin
from project.models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title')
    list_display_links = ('title',)
    list_filter = ('owner',)

admin.site.register(Project, ProjectAdmin)
