from rest_framework import serializers

from items.models import Item, ItemAttributeEffect, ItemType


class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class ItemListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field="name")
    item_type = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Item
        fields = ["name", "description", "category", "item_type"]


class ItemAttributeEffectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemAttributeEffect
        fields = "__all__"
