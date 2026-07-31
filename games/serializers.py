from rest_framework import serializers

from characters.models import Character
from .models import Action, ActionAttributeRequirement, CharacterAction

class ActionAttributeRequirementSerializer(serializers.ModelSerializer):
    attribute_code = serializers.ReadOnlyField(source='attribute.code')
    attribute_name = serializers.ReadOnlyField(source='attribute.name')

    class Meta:
        model = ActionAttributeRequirement
        fields = ['id', 'attribute', 'attribute_code', 'attribute_name', 'weight', 'difficulty_delta']


class ActionSerializer(serializers.ModelSerializer):
    requirements = ActionAttributeRequirementSerializer(many=True, read_only=True)

    class Meta:
        model = Action
        fields = [
            'id', 'code', 'name', 'description',
            'difficulty', 'type', 'active',
            'requirements',
        ]

class CharacterActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CharacterAction
        fields = ['action', 'character', 'result']
        read_only_fields = ['result']