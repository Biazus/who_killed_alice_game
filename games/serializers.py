from rest_framework import serializers

from characters.models import Character

from .models import (Act, Action, ActionAttributeRequirement,
                     ActionItemRequirement, CharacterAction, Scene,
                     SceneAction, CharacterProgressOnAct)

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

# Serializer para SceneAction, agora incluindo os detalhes da Action
class SceneActionSerializer(serializers.ModelSerializer):
    action = ActionSerializer(read_only=True) # Continua incluindo Action, pois é um detalhe pequeno e importante para a ação em si

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
            "scene", # Incluir o ID da cena à qual pertence
        ]

# Serializer para Scene, agora sem aninhar SceneAction
class SceneSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="scene-detail", lookup_field="pk") # Comentado, se não estiver em uso
    # scene_actions agora será buscado separadamente pelo frontend
    # scene_actions = SceneActionSerializer(many=True, read_only=True) # REMOVIDO

    class Meta:
        model = Scene
        fields = "__all__" # Retorna todos os campos, incluindo o ID do Act

# Serializer para Act, agora sem aninhar Scenes
class ActSerializer(serializers.ModelSerializer):
    # scenes agora será buscado separadamente pelo frontend
    # scenes = SceneSerializer(many=True, read_only=True) # REMOVIDO

    class Meta:
        model = Act
        fields = "__all__"

# Serializer para CharacterProgressOnAct, agora com Act e Scene completos, mas sem aninhamento profundo
class CharacterProgressOnActSerializer(serializers.ModelSerializer):
    # Usamos os serializers completos para Act e Scene aqui,
    # pois o progresso *sempre* precisa saber qual é o ato e a cena atual.
    # A diferença é que ActSerializer e SceneSerializer não aninham mais suas relações.
    act = ActSerializer(read_only=True)
    current_scene = SceneSerializer(read_only=True)

    class Meta:
        model = CharacterProgressOnAct
        fields = "__all__"