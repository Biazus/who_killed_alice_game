import random

from django.shortcuts import render, get_object_or_404
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (Act, Action, ActionItemRequirement, CharacterAction,
                     Scene, SceneAction, CharacterProgressOnAct)
from characters.models import Character
from .serializers import (ActionItemRequirementSerializer, ActionSerializer,
                          ActSerializer, CharacterActionSerializer, CharacterProgressOnActSerializer,
                          SceneActionSerializer, SceneSerializer)
from .services import ActionService # Certifique-se de que ActionService está definido ou remova se não for usar

class ActionViewSet(viewsets.ModelViewSet):
    serializer_class = ActionSerializer

    def get_queryset(self):
        return Action.objects.all()

class CharacterActionViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterActionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        character = serializer.validated_data["character"]
        action = serializer.validated_data["action"]
        action_service = ActionService(character) # <-- Verifique se ActionService está definido
        action_result = action_service.resolve_action_min_gate(action.code)
        serializer.save(result=action_result)
        # Customize response data
        return Response(action_result, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return CharacterAction.objects.all()

class ActionItemRequirementViewSet(viewsets.ModelViewSet):
    serializer_class = ActionItemRequirementSerializer
    queryset = ActionItemRequirement.objects.all()

class SceneActionViewSet(viewsets.ModelViewSet):
    serializer_class = SceneActionSerializer
    queryset = SceneAction.objects.all()

class CharacterProgressOnActViewSet(viewsets.ModelViewSet):
    queryset = CharacterProgressOnAct.objects.all()
    serializer_class = CharacterProgressOnActSerializer

    def get_queryset(self):
        # Permite filtrar por personagem, se necessário
        character_id = self.request.query_params.get('character_id')
        if character_id:
            return self.queryset.filter(character__id=character_id)
        return self.queryset

class SceneViewSet(viewsets.ModelViewSet):
    serializer_class = SceneSerializer
    queryset = Scene.objects.all()

class ActViewSet(viewsets.ModelViewSet):
    serializer_class = ActSerializer
    queryset = Act.objects.all()

class SceneActionSelectView(APIView):
    """
    Endpoint para selecionar uma ação em uma cena e avançar no jogo.
    Também inicia um novo progresso se não houver um ativo.
    """

    def _get_or_create_character_progress(self, character_id: int) -> CharacterProgressOnAct:
        """
        Tenta obter o progresso ativo do personagem. Se não existir, cria um novo
        com o primeiro ato e a primeira cena.
        """
        character = get_object_or_404(Character, id=character_id)

        # Tenta encontrar um progresso ativo (não finalizado)
        character_progress = CharacterProgressOnAct.objects.filter(
            character=character,
            finished=False
        ).first()

        if not character_progress:
            # Se não houver progresso ativo, inicia um novo
            first_act = Act.objects.order_by('id').first() # Ou por um campo 'order' se você tiver
            if not first_act:
                raise ValueError("Nenhum Ato configurado no sistema para iniciar o jogo.")

            # Pega a primeira cena do primeiro ato, ordenada pelo campo 'order'
            first_scene_of_act = first_act.scenes.order_by('order').first() # <-- Ajustado para usar related_name 'scenes' e 'order'
            if not first_scene_of_act:
                raise ValueError(f"O Ato '{first_act.title}' não possui cenas configuradas.")

            with transaction.atomic():
                character_progress = CharacterProgressOnAct.objects.create(
                    character=character,
                    act=first_act, # <-- Adicionado o act
                    current_scene=first_scene_of_act,
                    finished=False
                )
            print(f"Novo progresso criado para {character.name} no Ato '{first_act.title}', Cena '{first_scene_of_act.title}'.")

        return character_progress

    def post(self, request, *args, **kwargs):

        character_id = request.data.get('character_id')
        scene_action_id = request.data.get('scene_action_id')

        if not character_id:
            return Response(
                {"detail": "character_id é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            character_progress = self._get_or_create_character_progress(character_id)
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Character.DoesNotExist:
            return Response(
                {"detail": "Personagem não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Se scene_action_id não for fornecido, significa que é a primeira requisição
        # para iniciar o jogo ou apenas obter o estado atual.
        if not scene_action_id:
            serializer = CharacterProgressOnActSerializer(character_progress)
            return Response(serializer.data, status=status.HTTP_200_OK)

        scene_action = get_object_or_404(SceneAction, id=scene_action_id)

        if scene_action.scene != character_progress.current_scene:
            return Response(
                {"detail": "A ação selecionada não pertence à cena atual do personagem."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # --- Lógica de Rolagem de Dado (Exemplo Básico) ---
        # Você expandirá isso com base nos atributos do personagem e dificuldade da ação.
        roll_result = random.randint(1, 20) # Simula um d20
        threshold = scene_action.action.difficulty if scene_action.action else 10 # Exemplo: dificuldade base

        next_scene = None
        message = ""

        if scene_action.action_type == 'P' and scene_action.action:
            if roll_result >= threshold:
                next_scene = scene_action.on_success
                message = f"Você rolou {roll_result} e obteve sucesso! Aventura continua..."
            elif scene_action.on_hard_fail and roll_result <= (threshold / 2): # Exemplo de falha crítica
                next_scene = scene_action.on_hard_fail
                message = f"Você rolou {roll_result} e falhou criticamente! Consequências inesperadas..."
            else:
                next_scene = scene_action.on_fail
                message = f"Você rolou {roll_result} e falhou. A história toma outro rumo..."
        else:
            # Se não for uma ação de jogador ou não tiver action associada,
            # assume-se que sempre avança para o sucesso (ou a próxima cena lógica)
            next_scene = scene_action.on_success
            message = "A história avança..."

        if not next_scene:
            # Se não houver uma cena de transição definida para o resultado,
            # pode significar o fim de um caminho ou um erro de configuração.
            # Você pode definir uma cena padrão de "fim de jogo" ou "fim de ato".
            character_progress.finished = True # Marca o progresso como finalizado
            character_progress.save()
            return Response(
                {"detail": f"{message} O caminho se encerra aqui. Progresso finalizado.", "finished": True},
                status=status.HTTP_200_OK
            )

        character_progress.current_scene = next_scene
        character_progress.save()

        serializer = CharacterProgressOnActSerializer(character_progress)
        response_data = serializer.data
        response_data['game_message'] = message # Adiciona a mensagem do jogo à resposta
        return Response(response_data, status=status.HTTP_200_OK)