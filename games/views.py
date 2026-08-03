from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Act, Action, ActionItemRequirement, CharacterAction, SceneAction, Scene
from .serializers import (ActionItemRequirementSerializer, ActionSerializer,
                          CharacterActionSerializer, SceneActionSerializer, SceneSerializer, ActSerializer)
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


class SceneViewSet(viewsets.ModelViewSet):
    serializer_class = SceneSerializer
    queryset = Scene.objects.all()


class ActViewSet(viewsets.ModelViewSet):
    serializer_class = ActSerializer
    queryset = Act.objects.all()