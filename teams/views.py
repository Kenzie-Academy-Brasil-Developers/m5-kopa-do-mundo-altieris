from rest_framework.views import APIView, Response, Request
from .models import Team
from django.forms.models import model_to_dict
from .utils import NegativeTitlesError, data_processing
import ipdb

class TeamView(APIView):
    def get(self, request: Request) -> Response:
        teams = Team.objects.all()
        
        teams_list = []
        
        for team in teams:
            teams_dict = model_to_dict(team)
            teams_list.append(teams_dict)
       
        return Response(teams_list, status=200)
    
    def post(self, request: Request) -> Response:
        try:
            data_processing(request.data)
        except NegativeTitlesError as err:
            return Response({"error": err.message}, status=400)
        
        team = Team.objects.create(**request.data)
        
        team_dict = model_to_dict(team)
        
        return Response(team_dict, status=201)
    
class TeamDetailView(APIView):
    def get(self, request: Request, team_id: int):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)
        
        team_dict = model_to_dict(team)
        
        return Response(team_dict, status=200)
    
    def delete(self, request: Request, team_id: int):
        try:
            team = Team.objects.get(id=team_id)
            team.delete()
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)
        
        
        return Response(status=204)
    
    def patch(self, request: Request, team_id: int):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)
        
        team.name = request.data.get('name', team.name)
        team.titles = request.data.get('titles', team.titles)
        team.top_scorer = request.data.get('top_scorer', team.top_scorer)
        team.fifa_code = request.data.get('fifa_code', team.fifa_code)
        team.first_cup = request.data.get('first_cup', team.first_cup)
        
        team.save()
        
        team_dict = model_to_dict(team)
        
        return Response(team_dict, status=200)