from django.db import models

from characters.models import Character


class Action(models.Model):
    code = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

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

    # quanto esse atributo pesa no cálculo
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
    item_type = models.ForeignKey("items.ItemType", on_delete=models.CASCADE)

    required = models.BooleanField(default=True)
    min_quantity = models.PositiveIntegerField(default=1)

    consumed_on_use = models.BooleanField(default=False)

    class Meta:
        unique_together = ("action", "item_type")

    def __str__(self):
        return f"{self.action.code} -> {self.item_type.code}"


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

    def __str__(self):
        return self.title


class Scene(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    initial = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    act = models.ForeignKey(Act, on_delete=models.CASCADE, related_name="scenes")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.act.title} - {self.title}"


class SceneAction(models.Model):
    class ActionType(models.TextChoices):
        PLAYER_ACTION = "P", "Player"
        HISTORY_ACTION = "H", "History"

    scene = models.ForeignKey(
        Scene, on_delete=models.CASCADE, related_name="scene_actions"
    )
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

    def __str__(self):
        return (
            f"[{self.scene.title if self.scene else 'N/A'}] {self.description[:50]}..."
        )


class CharacterProgressOnAct(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="progresses"
    )
    act = models.ForeignKey(
        Act, on_delete=models.CASCADE, related_name="progresses_on_act"
    )
    current_scene = models.ForeignKey(
        "games.Scene", on_delete=models.CASCADE, related_name="current_progresses"
    )
    finished = models.BooleanField(default=False)

    class Meta:
        unique_together = ("character", "act")

    def __str__(self):
        return f"{self.character.name} - {self.act.title} (Scene: {self.current_scene.title})"
