from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from gamerraterapi.models import Game_Picture, Game
from django.contrib.auth.models import User
import uuid
import base64
from django.core.files.base import ContentFile


class ImageView(ViewSet):
    def create(self, request):
        user=request.auth.user
        image = Game_Picture()
        format, imgstr = request.data["game_image"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["game_id"]}-{uuid.uuid4()}.{ext}')
        image.image = data
        game = Game.objects.get(pk=request.data["game_id"])
        image.game = game
        try:
            image.save()
            serializer = ImageSerializer(image, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        try:
            image = Game_Picture.objects.get(pk=pk)
            serializer = ImageSerializer(image, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        images = Game_Picture.objects.all()
        game_id = self.request.query_params.get('gameId', None)
        if game_id is not None:
            images = images.filter(game__id = game_id)
        serializer = ImageSerializer(
            images, many=True, context={'request': request})
        return Response(serializer.data)
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game_Picture
        fields = ('id', 'image')