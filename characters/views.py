from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from characters.models import (Character, CharacterModifier,
                               CharacterModifierAttribute, Inventory)
from characters.serializers import (CharacterDetailSerializer,
                                    CharacterListSerializer,
                                    CharacterModifierAttributeListSerializer,
                                    CharacterModifierAttributeSerializer,
                                    CharacterModifierSerializer,
                                    CharacterSerializer,
                                    InventoryListSerializer,
                                    InventorySerializer)
from characters.services import CharacterService
from core.permissions import IsOwnerOrReadOnly


class CharacterViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

    filterset_fields = ["level"]

    ordering_fields = ["level", "current_health", "created", "name"]
    ordering = ["-created"]

    search_fields = ["name"]

    def get_queryset(self):
        return Character.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return CharacterListSerializer
        elif self.action == "retrieve":
            return CharacterDetailSerializer
        return CharacterSerializer

    def perform_create(self, serializer):
        character = serializer.save(owner=self.request.user)
        service = CharacterService(character)
        service.attach_random_modifiers_to_character(num_modifiers=3)
        service.attach_random_items_to_character(num_items=2)

    @action(detail=True, methods=["post"])
    def heal(self, request, pk=None):
        character = self.get_object()
        service = CharacterService(character)
        service.heal(request.data.get("amount"))
        return Response("Healed", status=200)

    @action(detail=True, methods=["post"])
    def reset(self, request, pk=None):
        character = self.get_object()
        service = CharacterService(character)
        service.reset()
        return Response("Reset", status=200)

    @action(detail=True, methods=["get"])
    def get_character_attribute_values(self, request, pk=None):
        character = self.get_object()
        service = CharacterService(character)
        service_response = service.get_character_attribute_values()
        return Response(service_response)

    @action(detail=True, methods=["get"])
    def get_character_effects_from_items(self, request, pk=None):
        character = self.get_object()
        service = CharacterService(character)
        service_response = service.get_character_attribute_from_items()
        return Response(service_response)


class CharacterModifierViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterModifierSerializer
    queryset = CharacterModifier.objects.all()


class CharacterModifierAttributeViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterModifierAttributeSerializer
    queryset = CharacterModifierAttribute.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CharacterModifierAttributeListSerializer
        return CharacterModifierAttributeSerializer


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return InventoryListSerializer
        return InventorySerializer
