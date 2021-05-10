from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from gamerraterapi.models import Game, Review
from django.contrib.auth.models import User


class ReviewView(ViewSet):
    def create(self, request):
        user=request.auth.user
        review = Review()
        game = Game.objects.get(pk=request.data["game"])
        review.title = request.data["title"]
        review.user = user
        review.game = game
        review.review = request.data["review"]
        review.rating = request.data["rating"]
        try:
            review.save()
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)       
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    def update(self, request, pk=None):
        user=request.auth.user
        review = Review.objects.get(pk=pk)
        review.title = request.data["title"]
        review.user = user
        review.review = request.data["review"]
        review.rating = request.data["rating"]
        review.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    def destroy(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            review.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def list(self, request):
        reviews = Review.objects.all()
        game_id = self.request.query_params.get('gameId', None)
        if game_id is not None:
            reviews = reviews.filter(game__id = game_id)
        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','id')
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Review
        fields = ('id', 'title','user','review','rating','game')
        depth = 1
