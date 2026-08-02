import random

from django.db.models import Sum

from characters.constants import BASE_ATTRIBUTE
from characters.services import CharacterService

from .models import Action


class ActionService:
    character = None

    def __init__(self, character):
        self.character = character

    def resolve_action_min_gate(self, action_code: str) -> dict:
        action = Action.objects.prefetch_related("requirements__attribute").get(
            code=action_code
        )
        reqs = action.requirements.all()

        if not reqs:
            raise ValueError(f"Action {action_code} has no attribute requirements")

        attr_values = []
        character_service = CharacterService(self.character)
        char_attr_values = character_service.get_character_attribute_values()
        for req in reqs:
            value = char_attr_values.get(req.attribute.code, BASE_ATTRIBUTE)
            attr_values.append(
                {
                    "req": req,
                    "value": value,
                }
            )

        # menor valor entre os atributos exigidos
        min_entry = min(attr_values, key=lambda x: x["value"])
        gate_value = min_entry["value"]
        total_difficulty = action.difficulty + sum(
            r["req"].difficulty_delta for r in attr_values
        )

        chance = max(0, min(100, gate_value - total_difficulty))
        roll = random.randint(1, 100)
        success = roll <= chance
        if not success:
            message = f"{min_entry['req'].attribute.name} não foi suficiente ao tentar {action.name}"
        else:
            message = f"Você conseguiu {action.name} com sucesso!"

        # resposta com detalhes
        return {
            "action_code": action.code,
            "action_name": action.name,
            "gate_attribute_code": min_entry["req"].attribute.code,
            "gate_attribute_name": min_entry["req"].attribute.name,
            "gate_value": gate_value,
            "total_difficulty": total_difficulty,
            "chance": chance,
            "roll": roll,
            "success": success,
            "attributes": [
                {
                    "attribute_code": e["req"].attribute.code,
                    "attribute_name": e["req"].attribute.name,
                    "value": e["value"],
                    "weight": e["req"].weight,
                    "difficulty_delta": e["req"].difficulty_delta,
                }
                for e in attr_values
            ],
            "message": message,
        }
