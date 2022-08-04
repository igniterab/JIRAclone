from django.contrib import admin
from django.urls import re_path, include

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^tasks/api/', include('tasks.urls')),
    re_path(r'^accounts/api/',include('accounts.urls')),
]
