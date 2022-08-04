from django.db import models
from django.utils import timezone
from accounts.models import MyUser as User


TASK_STATUS = (
    ("todo", "TODO"),
    ("in_progress", "IN_PROGRESS"),
    ("qc", "QC"),
    ("uat", "UAT"),
    ("ready_for_demo", "READY_FOR_DEMO"),
    ("ready_for_prod_release", "READY_FOR_PROD_RELEASE"),
    ("done", "DONE"),
    ("cancelled", "CANCELLED"),
)

PRIORITY = (
    ("low", "LOW"),
    ("medium", "MEDIUM"),
    ("high", "HIGH"),
)

TASK_TYPE = (
    ("bug", "BUG"),
    ("task", "TASK"),
)


class Team(models.Model):
    name = models.CharField(max_length=20, blank=False, unique=True)
    team_leader = models.ForeignKey(User, related_name='team_leader',limit_choices_to={'groups__name': "TeamLeader"} ,on_delete=models.CASCADE)
    team_memebers = models.ManyToManyField(User, limit_choices_to={'groups__name': "TeamMember"})
    created_at = models.DateTimeField(editable=False, default=timezone.localtime(timezone.now()))
    modified_at = models.DateTimeField(default=timezone.localtime(timezone.now()))

    def __str__(self):
        return str(self.name)
        

class Task(models.Model):
    name = models.CharField(max_length=200, blank=False)
    task_no = models.AutoField(primary_key=True)
    description = models.CharField(max_length=800, blank=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT)
    sprint = models.IntegerField()
    type_of_task = models.CharField(max_length=4, choices=TASK_TYPE, default='task')
    status = models.CharField(max_length=22, choices=TASK_STATUS, default='todo')
    priority = models.CharField(max_length=6, choices=PRIORITY, default='medium')
    created_at = models.DateTimeField(editable=False, default=timezone.localtime(timezone.now()))
    modified_at = models.DateTimeField(default=timezone.localtime(timezone.now()))

    def __str__(self):
        return str(self.name)
    


class Comment(models.Model):
  content = models.TextField(blank=False)
  task = models.ForeignKey(Task, on_delete=models.CASCADE)
  user = models.ForeignKey(User, limit_choices_to={'groups__name__in': ["TeamMember", "TeamLeader"]}, on_delete=models.CASCADE)
  created_at = models.DateTimeField(editable=False, default=timezone.localtime(timezone.now()))
  modified_at = models.DateTimeField(default=timezone.localtime(timezone.now()))
  
  def __str__(self):
    return str(self.content)
