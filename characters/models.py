from django.db import models

from django.conf import settings

from items.models import Item
from modifiers.models import Modifier, Attribute


class Character(models.Model):
    male = 'male'
    female = 'female'
    GENDER_CHOICES = (
        (male, 'Male'),
        (female, 'Female'),
    )

    name = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
    )

    age = models.IntegerField()
    level = models.IntegerField(default=1)
    current_health = models.IntegerField(default=100)
    max_health = models.IntegerField(default=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('owner', 'name',)
    def __str__(self):
        return f'{self.name} (lvl {self.level})'


class CharacterModifier(models.Model):
    character = models.ForeignKey('Character', on_delete=models.CASCADE, related_name='modifiers')
    modifier = models.ForeignKey(Modifier, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('character', 'modifier')

    def __str__(self):
        return f'{self.character} - {self.modifier}'


class CharacterModifierAttribute(models.Model):
    character_modifier = models.ForeignKey(
        CharacterModifier,
        on_delete=models.CASCADE,
        related_name='attribute_modifiers'
    )
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    final_value = models.IntegerField()  # +12, -7 etc.

    class Meta:
        unique_together = ('character_modifier', 'attribute')

    def __str__(self):
        return f'{self.character_modifier} - {self.attribute}'


class Inventory(models.Model):
    character = models.ForeignKey('Character', on_delete=models.CASCADE, related_name='inventory')
    items = models.ManyToManyField(Item, related_name='inventories')