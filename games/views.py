from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from django.shortcuts import render

from .models import Action, CharacterAction
from .serializers import ActionSerializer, CharacterActionSerializer
from .services import ActionService
from characters.models import Character


class ActionViewSet(viewsets.ModelViewSet):
    serializer_class = ActionSerializer

    def get_queryset(self):
        return Action.objects.all()

class CharacterActionViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterActionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        character = serializer.validated_data['character']
        action = serializer.validated_data['action']
        action_service = ActionService(character)
        action_result = action_service.resolve_action_min_gate(action.code)
        serializer.save(result=action_result)
        # Customize response data
        return Response(action_result, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return CharacterAction.objects.all()