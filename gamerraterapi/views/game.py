from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from gamerraterapi.models import Game, Category
from django.contrib.auth.models import User
from django.db.models import Q


class GameView(ViewSet):
    def create(self, request):
        user=request.auth.user
        game = Game()
        game.title = request.data["title"]
        game.creator = user
        game.description = request.data["description"]
        game.designer = request.data["designer"]
        game.year = request.data["year"]
        game.players = request.data["players"]
        game.age = request.data["age"]
        game.time = request.data["time"]
        try:
            game.save()
            categories = Category.objects.in_bulk(request.data["categories"])
            game.category_set.set(categories)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    def update(self, request, pk=None):
        user=request.auth.user
        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.creator = user
        game.description = request.data["description"]
        game.designer = request.data["designer"]
        game.year = request.data["year"]
        game.players = request.data["players"]
        game.age = request.data["age"]
        game.time = request.data["time"]
        categories = Category.objects.in_bulk(request.data["categories"])
        game.category_set.set(categories)
        game.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    def destroy(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            game.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def list(self, request):
        games = Game.objects.all()
        search_text = self.request.query_params.get('q', None)
        sort_text = self.request.query_params.get('orderby', None)
        if search_text is not None:
            games = Game.objects.filter(Q(title__contains=search_text) | Q(description__contains=search_text) | Q(designer__contains=search_text))
        if sort_text is not None:
            games = Game.objects.order_by()

        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        
class GameSerializer(serializers.ModelSerializer):
    creator = UserSerializer(many=False)
    class Meta:
        model = Game
        fields = ('id', 'title','creator','description','designer','year','players','age','time','category_set','average_rating')
        depth = 1
