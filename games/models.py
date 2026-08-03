from django.db import models

from characters.models import Character


class Action(models.Model):
    code = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    # opcional: tipo/categoria da ação
    type = models.CharField(max_length=50, blank=True)

    difficulty = models.IntegerField(default=0)  # dificuldade "global" da ação
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ActionAttributeRequirement(models.Model):
    action = models.ForeignKey(
        "games.Action", on_delete=models.CASCADE, related_name="requirements"
    )
    attribute = models.ForeignKey("modifiers.Attribute", on_delete=models.CASCADE)

    # quanto esse atributo pesa no cálculo (default 1.0)
    weight = models.FloatField(default=1.0)

    # opcional: ajuste de dificuldade específico deste atributo
    difficulty_delta = models.IntegerField(default=0)

    class Meta:
        unique_together = ("action", "attribute")

    def __str__(self):
        return f"{self.action.code} -> {self.attribute.code} (w={self.weight})"


class CharacterAction(models.Model):
    action = models.ForeignKey(
        "games.Action", on_delete=models.CASCADE, related_name="actions"
    )
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    result = models.JSONField(default=dict)


class ActionItemRequirement(models.Model):
    action = models.ForeignKey(
        "games.Action", on_delete=models.CASCADE, related_name="item_requirements"
    )
    item_type = models.ForeignKey(
        "items.ItemType", on_delete=models.CASCADE  # ajuste app_label
    )

    required = models.BooleanField(default=True)
    # opcional: quantidade mínima
    min_quantity = models.PositiveIntegerField(default=1)

    consumed_on_use = models.BooleanField(default=False)

    class Meta:
        unique_together = ("action", "item_type")

    def __str__(self):
        return f"{self.action.code} -> {self.item_type.code}"


class CharacterProgressOnAct(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    current_scene = models.ForeignKey("games.Scene", on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)

    class Meta:
        unique_together = ("character", "current_scene")


class Act(models.Model):
    class Rewards(models.TextChoices):
        MODIFIER = "MO", "Modifier"
        ITEM = "IT", "Item"
        BADGE = "BA", "Badge"

    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    reward_type = models.CharField(
        choices=Rewards.choices, max_length=50, default=Rewards.MODIFIER
    )
    reward_id = models.IntegerField(default=1)  # TODO sort later


class Scene(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    initial = models.BooleanField(default=False)
    description = models.TextField(blank=True)


class SceneAction(models.Model):
    class ActionType(models.TextChoices):
        PLAYER_ACTION = "P", "Player"
        HISTORY_ACTION = "H", "History"

    scene = models.ForeignKey(Scene, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    action_type = models.CharField(
        choices=ActionType.choices, max_length=1, default=ActionType.HISTORY_ACTION
    )
    # action que será testada na "sorte"
    action = models.ForeignKey(Action, on_delete=models.CASCADE, null=True, blank=True)
    # action que nao é testada, apenas influencia historia
    history_action = models.CharField(max_length=100, null=True, blank=True)
    on_fail = models.ForeignKey(
        "games.Scene",
        on_delete=models.CASCADE,
        related_name="failed_from",
        null=True,
        blank=True,
    )
    on_success = models.ForeignKey(
        "games.Scene",
        on_delete=models.CASCADE,
        related_name="succeeded_from",
        null=True,
        blank=True,
    )
    on_hard_fail = models.ForeignKey(
        "games.Scene",
        on_delete=models.CASCADE,
        related_name="hard_failed_from",
        null=True,
        blank=True,
    )
