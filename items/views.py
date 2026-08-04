from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from items.models import Item, ItemAttributeEffect, ItemType
from items.serializers import (
    ItemAttributeEffectSerializer,
    ItemListSerializer,
    ItemSerializer,
    ItemTypeSerializer,
)


class ItemTypeViewSet(viewsets.ModelViewSet):
    queryset = ItemType.objects.all()
    serializer_class = ItemTypeSerializer


class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = []
    ordering_fields = ["name"]
    ordering = []
    search_fields = ["name"]

    def get_queryset(self):
        return Item.objects.all()  # filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ItemListSerializer
        return ItemSerializer


class ItemAttributeEffectViewSet(viewsets.ModelViewSet):
    queryset = ItemAttributeEffect.objects.all()
    serializer_class = ItemAttributeEffectSerializer
