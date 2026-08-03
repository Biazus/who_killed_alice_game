from django.urls import include, path
from rest_framework.routers import DefaultRouter

from characters.views import (CharacterModifierAttributeViewSet,
                              CharacterModifierViewSet, CharacterViewSet,
                              InventoryViewSet)
from games.views import (ActionItemRequirementViewSet, ActionViewSet,
                         CharacterActionViewSet, ActViewSet, SceneViewSet, SceneActionViewSet,
                         CharacterProgressOnActViewSet, SceneActionSelectView) # <-- Adicionado CharacterProgressOnActViewSet e SceneActionSelectView
from items.views import (ItemAttributeEffectViewSet, ItemTypeViewSet,
                         ItemViewSet)
from modifiers.views import (AttributeViewSet, ModifierAttributeEffectViewSet,
                             ModifierCategoryViewSet, ModifierViewSet)

router = DefaultRouter()
# characters app
router.register(r"characters", CharacterViewSet, basename="character")
router.register(r"inventories", InventoryViewSet, basename="inventory")
router.register(
    r"characters_modifiers", CharacterModifierViewSet, basename="character_modifier"
)
router.register(
    r"characters_modifiers_attributes",
    CharacterModifierAttributeViewSet,
    basename="character_modifier_attribute",
)
# items app
router.register(r"item_types", ItemTypeViewSet, basename="item_type")
router.register(r"items", ItemViewSet, basename="item")
router.register(
    r"item_attribute_effects",
    ItemAttributeEffectViewSet,
    basename="item_attribute_effect",
)
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
router.register(
    r"acts", ActViewSet, basename="act", # <-- Alterado para 'acts'
)
router.register(
    r"scenes", SceneViewSet, basename="scene", # <-- Alterado para 'scenes'
)
router.register(
    r"scene_actions",
    SceneActionViewSet,
    basename="scene_action",
)
router.register(
    r"character_progresses", CharacterProgressOnActViewSet, basename="character_progress" # <-- Adicionado registro
)

urlpatterns = [
    path("", include(router.urls)),
    path("scene_action_select/", SceneActionSelectView.as_view(), name="scene_action_select"), # <-- Adicionado endpoint para APIView
]