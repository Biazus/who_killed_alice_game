from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from characters.models import Character, Inventory, CharacterModifier, CharacterModifierAttribute
from core.permissions import IsOwnerOrReadOnly
from characters.serializers import CharacterDetailSerializer, CharacterSerializer, CharacterListSerializer, \
     CharacterModifierSerializer, InventorySerializer, CharacterModifierAttributeSerializer
from characters.services import CharacterService

class CharacterViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]

    filterset_fields = ['level']

    ordering_fields = ['level', 'current_health', 'created', 'name']
    ordering = ['-created']

    search_fields = ['name']
    def get_queryset(self):
        return Character.objects.filter(
            owner=self.request.user
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return CharacterListSerializer
        elif self.action == 'retrieve':
            return CharacterDetailSerializer
        return CharacterSerializer

    def perform_create(self, serializer):
        character = serializer.save(owner=self.request.user)
        service = CharacterService(character)
        service.attach_random_modifiers_to_character(num_modifiers=3)

    @action(detail=True, methods=['post'])
    def heal(self, request, pk=None):
        character = self.get_object()
        service = CharacterService(character)
        service.heal(request.data.get("amount"))
        return Response("Healed", status=200)

    @action(detail=True, methods=['post'])
    def reset(self, request, pk=None):
        character = self.get_object()
        service = CharacterService(character)
        service.reset()
        return Response("Reset", status=200)

    @action(detail=True, methods=['get'])
    def get_character_attribute_values(self, request, pk=None):
        character = self.get_object()
        service = CharacterService(character)
        service_response = service.get_character_attribute_values()
        return Response(service_response)

class CharacterModifierViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterModifierSerializer
    queryset = CharacterModifier.objects.all()


class CharacterModifierAttributeViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterModifierAttributeSerializer
    queryset = CharacterModifierAttribute.objects.all()

class InventoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()