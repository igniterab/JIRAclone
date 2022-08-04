from django.urls import re_path
from .views import TaskView, TeamView, CommentView


urlpatterns = [
    re_path(r'^task/$', TaskView.as_view(), name='task'),
    re_path(r'^teams/', TeamView.as_view(), name='teams'),
    re_path(r'^comments/', CommentView.as_view(), name='comments'),
]