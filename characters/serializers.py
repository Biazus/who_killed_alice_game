from rest_framework import serializers

from items.serializers import ItemSerializer
from modifiers.serializers import ModifierSerializer

from .models import (Character, CharacterModifier, CharacterModifierAttribute,
                     Inventory)


class CharacterModifierSerializer(serializers.ModelSerializer):
    modifier = ModifierSerializer()

    class Meta:
        model = CharacterModifier
        fields = ["modifier"]


class CharacterDetailSerializer(serializers.ModelSerializer):
    modifiers = CharacterModifierSerializer(many=True)

    class Meta:
        model = Character
        fields = "__all__"


class CharacterModifierAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterModifierAttribute
        fields = "__all__"


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = [
            "name",
            "age",
            "gender",
            "modifiers",
        ]
        read_only_fields = ["modifiers"]

    def validate_age(self, value):
        if value < 0 or value > 50:
            raise serializers.ValidationError("Idade escolhida invalida (max: 50)")
        return value

    def validate_name(self, value):
        value = value.title()
        if Character.objects.filter(name__icontains=value).exists():
            raise serializers.ValidationError("Nome ja cadastrado")
        return value


class InventorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    character = CharacterSerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = "__all__"


class CharacterListSerializer(serializers.HyperlinkedModelSerializer):
    modifiers = CharacterModifierSerializer(many=True, read_only=True)
    owner = serializers.CharField(source="owner.username", allow_null=True)

    class Meta:
        model = Character
        fields = ["url", "id", "name", "level", "owner", "modifiers"]
        extra_kwargs = {
            "url": {"view_name": "character-detail"}  # Matches default router naming
        }
