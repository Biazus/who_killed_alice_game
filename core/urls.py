from django.urls import include, path
from rest_framework.routers import DefaultRouter

from characters.views import (CharacterModifierAttributeViewSet,
                              CharacterModifierViewSet, CharacterViewSet,
                              InventoryViewSet)
from games.views import (ActionItemRequirementViewSet, ActionViewSet,
                         CharacterActionViewSet)
from items.views import ItemTypeViewSet, ItemViewSet
from modifiers.views import (AttributeViewSet, ModifierAttributeEffectViewSet,
                             ModifierCategoryViewSet, ModifierViewSet)

router = DefaultRouter()
# characters app
router.register(r"characters", CharacterViewSet, basename="character")
router.register(r"inventories", InventoryViewSet, basename="inventory")
router.register(
    r"characters/modifiers", CharacterModifierViewSet, basename="character_modifier"
)
router.register(
    r"characters/modifiers_attributes",
    CharacterModifierAttributeViewSet,
    basename="character_modifier_attribute",
)
# items app
router.register(r"item_types", ItemTypeViewSet, basename="item_type")
router.register(r"items", ItemViewSet, basename="item")
# modifiers app
router.register(r"categories", ModifierCategoryViewSet, basename="modifier_category")
router.register(r"modifiers", ModifierViewSet, basename="modifier")
router.register(r"attributes", AttributeViewSet, basename="attribute")
router.register(
    r"modifier_attribute_effects",
    ModifierAttributeEffectViewSet,
    basename="modifier_attribute_effect",
)
# games app
router.register(r"actions", ActionViewSet, basename="action")
router.register(
    r"character_actions", CharacterActionViewSet, basename="character_action"
)
router.register(
    r"action_item_requirement",
    ActionItemRequirementViewSet,
    basename="action_item_requirement",
)

urlpatterns = [
    path("", include(router.urls)),
]
