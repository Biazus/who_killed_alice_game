from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import (Act, Action, ActionItemRequirement, CharacterAction,
                     Scene, SceneAction, CharacterProgressOnAct)
from .serializers import (ActionItemRequirementSerializer, ActionSerializer,
                          ActSerializer, CharacterActionSerializer, CharacterProgressOnActSerializer,
                          SceneActionSerializer, SceneSerializer)
from .services import ActionService


class ActionViewSet(viewsets.ModelViewSet):
    serializer_class = ActionSerializer

    def get_queryset(self):
        return Action.objects.all()


class CharacterActionViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterActionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        character = serializer.validated_data["character"]
        action = serializer.validated_data["action"]
        action_service = ActionService(character)
        action_result = action_service.resolve_action_min_gate(action.code)
        serializer.save(result=action_result)
        # Customize response data
        return Response(action_result, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return CharacterAction.objects.all()


class ActionItemRequirementViewSet(viewsets.ModelViewSet):
    serializer_class = ActionItemRequirementSerializer
    queryset = ActionItemRequirement.objects.all()


class SceneActionViewSet(viewsets.ModelViewSet):
    serializer_class = SceneActionSerializer
    queryset = SceneAction.objects.all()


class CharacterProgressOnActViewSet(viewsets.ModelViewSet):
    queryset = CharacterProgressOnAct.objects.all()
    serializer_class = CharacterProgressOnActSerializer

    def get_queryset(self):
        # Permite filtrar por personagem, se necessário
        character_id = self.request.query_params.get('character_id')
        if character_id:
            return self.queryset.filter(character__id=character_id)
        return self.queryset


class SceneViewSet(viewsets.ModelViewSet):
    serializer_class = SceneSerializer
    queryset = Scene.objects.all()


class ActViewSet(viewsets.ModelViewSet):
    serializer_class = ActSerializer
    queryset = Act.objects.all()
