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
        'games.Action',
        on_delete=models.CASCADE,
        related_name='requirements'
    )
    attribute = models.ForeignKey('modifiers.Attribute', on_delete=models.CASCADE)

    # quanto esse atributo pesa no cálculo (default 1.0)
    weight = models.FloatField(default=1.0)

    # opcional: ajuste de dificuldade específico deste atributo
    difficulty_delta = models.IntegerField(default=0)

    class Meta:
        unique_together = ('action', 'attribute')

    def __str__(self):
        return f'{self.action.code} -> {self.attribute.code} (w={self.weight})'


class CharacterAction(models.Model):
    action = models.ForeignKey(
        'games.Action', on_delete=models.CASCADE, related_name='actions'
    )
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    result = models.JSONField(default=dict)