from django.shortcuts import render
from rest_framework import viewsets

from modifiers.models import (
    Attribute,
    Modifier,
    ModifierAttributeEffect,
    ModifierCategory,
)
from modifiers.serializers import (
    AttributeSerializer,
    ModifierAttributeEffectSerializer,
    ModifierCategorySerializer,
    ModifierSerializer,
)


# Create your views here.
class ModifierViewSet(viewsets.ModelViewSet):
    queryset = Modifier.objects.all()
    serializer_class = ModifierSerializer


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class ModifierAttributeEffectViewSet(viewsets.ModelViewSet):
    queryset = ModifierAttributeEffect.objects.all()
    serializer_class = ModifierAttributeEffectSerializer


class ModifierCategoryViewSet(viewsets.ModelViewSet):
    queryset = ModifierCategory.objects.all()
    serializer_class = ModifierCategorySerializer
