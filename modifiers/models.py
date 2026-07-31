from django.db import models


class ModifierCategory(models.Model):
    name = models.CharField(max_length=100)

class Modifier(models.Model):
    """
    Representa algo como 'Som de Orvalho', 'Bota Pesada', 'Língua de Chuva' etc.
    Pode ser vantagem ou desvantagem.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    # opcional: tag para tipo (furtividade, social etc.)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(
        'ModifierCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='modifiers',
    )

    def __str__(self):
        return self.name


class Attribute(models.Model):
    """
    Ex.: 'noise_walk', 'noise_lockpick', 'stealth_urban', 'persuasion', etc.
    """
    code = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class ModifierAttributeEffect(models.Model):
    IMPACT_SIGN_CHOICES = (
        ('+', 'Positive'),
        ('-', 'Negative'),
    )

    IMPACT_INTENSITY_CHOICES = (
        ('low', 'Low'),
        ('mid', 'Medium'),
        ('high', 'High'),
    )

    modifier = models.ForeignKey('Modifier', on_delete=models.CASCADE, related_name='attribute_effects')
    attribute = models.ForeignKey('Attribute', on_delete=models.CASCADE)
    sign = models.CharField(max_length=1, choices=IMPACT_SIGN_CHOICES)
    intensity = models.CharField(max_length=10, choices=IMPACT_INTENSITY_CHOICES)

    class Meta:
        unique_together = ('modifier', 'attribute')

    def __str__(self):
        return f'{self.modifier} -> {self.attribute.code} ({self.sign},{self.intensity})'