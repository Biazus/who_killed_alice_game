from rest_framework import serializers

from characters.models import Character

from .models import (Act, Action, ActionAttributeRequirement,
                     ActionItemRequirement, CharacterAction, Scene,
                     SceneAction)


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


class SceneSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="scene-detail", lookup_field="pk"
    )

    class Meta:
        model = Scene
        fields = "__all__"


class SceneActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SceneAction
        fields = "__all__"


class ActSerializer(serializers.ModelSerializer):
    class Meta:
        model = Act
        fields = "__all__"
