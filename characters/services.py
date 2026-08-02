import random
from collections import Counter

from django.db.models import Sum

from characters.constants import ATTRIBUTE_CAP, BASE_ATTRIBUTE
from items.models import Item, ItemAttributeEffect
from modifiers.models import Attribute, Modifier, ModifierAttributeEffect

from .models import CharacterModifier, CharacterModifierAttribute, Inventory

MODIFIER_INTENSITY_RANGE = {
    "low": (1, 4),
    "mid": (5, 9),
    "high": (10, 14),
}


def roll_modifier_value(intensity: str, sign: str) -> int:
    lo, hi = MODIFIER_INTENSITY_RANGE[intensity]
    value = random.randint(lo, hi)
    return value if sign == "+" else -value


class CharacterService(object):
    character = None

    def __init__(self, character):
        super(CharacterService, self).__init__()
        self.character = character

    def heal(self, amount):
        if not amount:
            self.character.current_health = self.character.max_health
        else:
            self.character.current_health = min(
                self.character.current_health + int(amount), self.character.max_health
            )
        self.character.save(update_fields=["current_health"])
        return self.character

    def reset(self):
        # TODO
        #self.character.current_health = self.character.max_health
        #self.character.level = 1
        return self.character

    def attach_random_items_to_character(self, num_items=1):
        inventory, _ = Inventory.objects.get_or_create(character=self.character)
        item_count = Item.objects.count()
        random_ints = random.sample(range(0, item_count), num_items)

        for i in random_ints:
            item = Item.objects.order_by("id")[i]
            inventory.items.add(item)

    def attach_random_modifiers_to_character(self, num_modifiers: int = None):
        """
        Sorteia 'num_modifiers' modifiers, garantindo categorias diferentes,
        atribui ao personagem e cria os CharacterModifierAttributeValue.
        """

        # 1. Descobrir categorias disponíveis
        # Exemplo: supor que Modifier tem um campo 'category' (CharField ou FK)
        modifiers = Modifier.objects.filter(active=True)

        # Agrupar modifiers por categoria
        by_category = {}
        for mod in modifiers:
            cat = mod.category or "uncategorized"
            by_category.setdefault(cat, []).append(mod)

        categories = list(by_category.keys())
        random.shuffle(categories)

        # Pegamos até 'num_modifiers' categorias distintas
        chosen_categories = categories[:num_modifiers]

        chosen_modifiers = []
        for cat in chosen_categories:
            pool = by_category[cat]
            if not pool:
                continue
            chosen_modifiers.append(random.choice(pool))

        for modifier in chosen_modifiers:
            cm = CharacterModifier.objects.create(
                character=self.character, modifier=modifier
            )
            for eff in modifier.attribute_effects.all():

                final_value = roll_modifier_value(eff.intensity, eff.sign)
                CharacterModifierAttribute.objects.create(
                    character_modifier=cm,
                    attribute=eff.attribute,
                    final_value=final_value,
                )

        return chosen_modifiers

    def get_character_attribute_values(self) -> dict:
        res = Counter(self.get_attribute_delta_from_modifiers())
        items = self.get_character_attribute_from_items()
        res.update(items)
        return res

    def get_attribute_delta_from_modifiers(self) -> dict[str, int]:
        qs = (
            CharacterModifierAttribute.objects.filter(
                character_modifier__character=self.character
            )
            .values("attribute__code")
            .annotate(total=Sum("final_value"))
        )
        return {row["attribute__code"]: row["total"] for row in qs}

    def get_character_attribute_from_items(self) -> dict[str, int]:
        inventory = Inventory.objects.prefetch_related(
            "items__attribute_effects",  # usa o related_name do ItemAttributeEffect
            "items__attribute_effects__attribute",
        ).get(character=self.character)

        attributes: dict[str, int] = {}

        for item in inventory.items.all():
            for effect in item.attribute_effects.all():
                key = effect.attribute.code
                delta = roll_modifier_value(effect.intensity, effect.sign)
                attributes[key] = attributes.get(key, 0) + delta

        return attributes
