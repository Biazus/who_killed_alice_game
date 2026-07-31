from rest_framework import serializers

from modifiers.models import ModifierAttributeEffect, Modifier, Attribute, ModifierCategory


class ModifierCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ModifierCategory
        fields = '__all__'

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'

class ModifierSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', allow_null=True)
    class Meta:
        model = Modifier
        fields = ['name', 'description', 'category']


class ModifierAttributeEffectSerializer(serializers.ModelSerializer):
    attribute = serializers.SlugRelatedField(slug_field='name', read_only=True)
    #modifier = serializers.SlugRelatedField(slug_field='name', read_only=True)
    modifier = ModifierSerializer()

    class Meta:
        model = ModifierAttributeEffect
        fields = '__all__'