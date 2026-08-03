from rest_framework import serializers

from characters.models import Character

from .models import (Act, Action, ActionAttributeRequirement,
                     ActionItemRequirement, CharacterAction, Scene,
                     SceneAction, CharacterProgressOnAct) # <-- Adicionado CharacterProgressOnAct

class ActionAttributeRequirementSerializer(serializers.ModelSerializer):
    attribute_code = serializers.ReadOnlyField(source="attribute.code")
    attribute_name = serializers.ReadOnlyField(source="attribute.name")

    class Meta:
        model = ActionAttributeRequirement
        fields = [
            "id",
            "attribute",
            "attribute_code",
            "attribute_name",
            "weight",
            "difficulty_delta",
        ]

class ActionSerializer(serializers.ModelSerializer):
    requirements = ActionAttributeRequirementSerializer(many=True, read_only=True)

    class Meta:
        model = Action
        fields = [
            "id",
            "code",
            "name",
            "description",
            "difficulty",
            "type",
            "active",
            "requirements",
        ]

class CharacterActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CharacterAction
        fields = ["action", "character", "result"]
        read_only_fields = ["result"]

class ActionItemRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionItemRequirement
        fields = "__all__"

class SceneActionSerializer(serializers.ModelSerializer):
    action = ActionSerializer(read_only=True)  # Inclui os detalhes da Action

    class Meta:
        model = SceneAction
        fields = [
            "id",
            "description",
            "action_type",
            "action",
            "history_action",
            "on_fail",
            "on_success",
            "on_hard_fail",
        ]

class SceneSerializer(serializers.ModelSerializer):
    #url = serializers.HyperlinkedIdentityField(
    #    view_name="scene-detail", lookup_field="pk"
    #) # <-- Comentado, pois não está sendo usado e pode causar erro se a view não existir
    scene_actions = SceneActionSerializer(many=True, read_only=True)  # Inclui as ações da cena

    class Meta:
        model = Scene
        fields = "__all__"

class ActSerializer(serializers.ModelSerializer):
    scenes = SceneSerializer(many=True, read_only=True)  # Inclui as cenas do ato
    class Meta:
        model = Act
        fields = "__all__"

class CharacterProgressOnActSerializer(serializers.ModelSerializer): # <-- Novo Serializer
    act = ActSerializer(read_only=True)
    current_scene = SceneSerializer(read_only=True)

    class Meta:
        model = CharacterProgressOnAct
        fields = "__all__"