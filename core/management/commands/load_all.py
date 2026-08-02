from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Carrega todas as fixtures necessárias de uma só vez'

    def handle(self, *args, **options):
        fixtures = [
            'attributes.json',
            'actions.json',
            'item_types.json',
            'modifier_categories.json',
            'items.json',
            'modifiers.json',
            'modifier_attribute_effects.json',
            'item_attribute_effects.json'
        ]

        for fixture in fixtures:
            self.stdout.write(f'Carregando {fixture}...')
            call_command('loaddata', fixture)

        self.stdout.write(self.style.SUCCESS('Todas as fixtures foram carregadas!'))

