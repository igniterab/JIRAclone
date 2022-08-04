from django.contrib import admin
from .models import Team, Task, Comment

class TeamAdmin(admin.ModelAdmin):
  list_display = ('name', 'created_at', 'modified_at')
  list_filter = ['created_at']
  search_fields = ['name']


class TaskAdmin(admin.ModelAdmin):
  list_display = ('task_no', 'name', 'sprint', 'status', 'type_of_task', 'created_at', 'modified_at')
  list_filter = ['created_at', 'sprint', 'status', 'type_of_task']
  search_fields = ['name', 'task_no']
  readonly_fields = ('task_no',)


class CommentAdmin(admin.ModelAdmin):
  list_display = ('user', 'content', 'created_at', 'modified_at')
  list_filter = ['created_at', 'user']
  search_fields = ['content', 'user']


admin.site.register(Team, TeamAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
