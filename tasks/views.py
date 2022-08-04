from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.models import MyUser
from .models import Team, Task, Comment
from django.utils import timezone
from .tasks import send_mail_func
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class TeamView(APIView):
    """
    List all Team, or create a new Team.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teams = list(Team.objects.all().values("name", "team_leader__name"))
        content = {'status': 1,'teams': teams}
        return Response(content, status=status.HTTP_200_OK)

    def post(self, request):
        name = request.data.get("name", None)
        team_leader = request.data.get("team_leader", None)
        
        if name is None:
            content = {'status': 0,'message': "Name is required to create team"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        if team_leader is None:
            content = {'status': 0,'message': 'Team Leader Name is required to create team'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            team_leader_obj = MyUser.objects.get(name=team_leader)
        except:
            content = {'status': 0,'message': f"Team Leader {team_leader} doesn't exists"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            team_obj, created = Team.objects.get_or_create(name=name, team_leader=team_leader_obj)
            if created:
                content = {'status': 1,'message': f"Team with name {name} created successfully"}
                return Response(content, status=status.HTTP_201_CREATED)
            else:
                content = {'status': 1,'message': f"Team with name {name} and leader {team_leader} already exists"}
                return Response(content, status=status.HTTP_200_OK)

        except Exception as e:
            content = {'status': 0,'message': f"Error occured: {e}"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

    def put(self, request): 
        pass

    def delete(self, request): 
        pass


class TaskView(APIView):
    """
    List all Tasks, or create a new Task.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = list(Task.objects.all().values())
        return Response({"tasks": tasks})

    def post(self, request):
        name = request.data.get("name", None)
        team_name = request.data.get("team_name", None)
        created_by = request.data.get("created_by", None)
        sprint = request.data.get("sprint", None)
        description = request.data.get("description", "some random text")
        
        if name is None:
            content = {'status': 0, 'message': "Name is required to create task"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        if team_name is None:
            content = {'status': 0, 'message': 'Team Name is required to create task'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        if created_by is None:
            content = {'status': 0, 'message': "Created by i.e creator name is required to create task"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        if sprint is None:
            content = {'status': 0, 'message': "sprint is required to create task"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            team_obj = Team.objects.get(name=team_name)
        except:
            content = {'status': 0, 'message': f"Team {team_name} doesn't exists"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            user_obj = MyUser.objects.get(name=created_by)
        except:
            content = {'status': 0, 'message': f"User {created_by} doesn't exists"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            task_obj, created = Task.objects.get_or_create(name=name, team=team_obj, description=description, sprint=sprint, created_by=user_obj)
            if created:
                content = {'status': 1,'message': f"Task with name {name} created successfully"}
                send_mail_func.delay(receipent_email=team_obj.team_leader.email, receipent_name=team_obj.team_leader.email)
                return Response(content, status=status.HTTP_201_CREATED)
            else:
                content = {'status': 1,'message': f"Task with name {name} and team {team_name} already exists"}
                return Response(content, status=status.HTTP_200_OK)

        except Exception as e:
            content = {'status': 0,'message': f"Error occured: {e}"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

    def put(self, request): 
        print(request._auth["user_id"])
        name = request.data.get("name", None)
        team_name = request.data.get("team_name", None)
        sprint = request.data.get("sprint", None)
        description = request.data.get("description", None)
        type_of_task = request.data.get("type_of_task", None)
        task_status = request.data.get("status", None)
        priority = request.data.get("priority", None)

        if name is None:
            content = {'status': 0, 'message': "Name is required to update task"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            task_obj = Task.objects.get(name=name)
        except Exception as e:
            content = {'status': 0,'message': f"Error occured: {e}"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        user_obj = request._user
        if(user_obj.groups.filter(name='TeamLeader').exists()):
            if team_name is not None:
                try:
                    team_obj = Team.objects.get(name=team_name)
                    task_obj.team_name = team_name
                except:
                    content = {'status': 0, 'message': f"Team {team_name} doesn't exists"}
                    return Response(content, status=status.HTTP_404_NOT_FOUND)
                
            if sprint is not None:
                task_obj.sprint = sprint

            if description is not None:
                task_obj.description = description

            if type_of_task is not None:
                task_obj.type_of_task = type_of_task

            if task_status is not None:
                task_obj.status = task_status

            if priority is not None:
                task_obj.priority = priority
            
            task_obj.modified_at = timezone.localtime(timezone.now())
            task_obj.save()
            
            content = {'status': 1, 'message': f"Task {name} updated successfully"}
            return Response(content, status=status.HTTP_200_OK)

        else:
            if status is not None:
                task_obj.status = status
            
            task_obj.modified_at = timezone.localtime(timezone.now())
            task_obj.save()

            content = {'status': 1, 'message': f"Task {name} updated successfully, only status is updated. According to your permissions"}
            return Response(content, status=status.HTTP_200_OK)

    def delete(self, request): 
        pass


class CommentView(APIView):
    """
    List all Comments, or create a new Comment.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        comment = list(Comment.objects.all().values("content", "task", "user"))
        return Response({"comments": comment})

    def post(self, request):
        pass

    def put(self, request): 
        pass

    def delete(self, request): 
        pass