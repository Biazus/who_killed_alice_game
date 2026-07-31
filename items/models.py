from django.db import models

from modifiers.models import Attribute, ModifierCategory

class Item(models.Model):
    MELEE = 'melee'
    RANGED = 'ranged'
    ITEM_TYPE_CHOICES = [
        (MELEE, 'Melee'),
        (RANGED, 'Ranged'),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    damage = models.PositiveIntegerField()
    weight = models.FloatField()
    created = models.DateTimeField(null=True, auto_now_add=True)
    category = models.ForeignKey(
        ModifierCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='items',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'


class ItemAttributeEffect(models.Model):
    IMPACT_SIGN_CHOICES = (
        ('+', 'Positive'),
        ('-', 'Negative'),
    )

    IMPACT_INTENSITY_CHOICES = (
        ('low', 'Low'),
        ('mid', 'Medium'),
        ('high', 'High'),
    )

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='attribute_effects')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    sign = models.CharField(max_length=1, choices=IMPACT_SIGN_CHOICES)
    intensity = models.CharField(max_length=10, choices=IMPACT_INTENSITY_CHOICES)

    class Meta:
        unique_together = ('item', 'attribute')

    def __str__(self):
        return f'{self.item} -> {self.attribute.code} ({self.sign},{self.intensity})'