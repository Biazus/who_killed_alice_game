import api from "../api";

export interface Modifier {
  name: string;
  description: string;
  category: string;
}

export interface CharacterModifier {
  id: number;
  modifier: Modifier;
  character: number;
}

export interface InventoryItem {
  id: number;
  name: string;
  description: string;
  weight: number;
  created?: string | null;
  item_type?: number;
  category?: number;
}

export interface CharacterInventory {
  id: number;
  items: InventoryItem[];
}

export interface Character {
  id: number;
  name: string;
  level: number;
  owner?: number | string;

  gender?: string;
  age?: number;
  current_health?: number;
  max_health?: number;

  modifiers: CharacterModifier[];
  inventory?: CharacterInventory[];

  created?: string;
  updated?: string;
}

// Novas interfaces para o jogo
export interface Action {
  id: number;
  code: string;
  name: string;
  description: string;
  difficulty: number;
  type: string;
  active: boolean;
  requirements: any[]; // Ajuste conforme ActionAttributeRequirementSerializer
}

export interface SceneAction {
  id: number;
  description: string;
  action_type: "P" | "H"; // Player Action ou History Action
  action: Action | null; // Detalhes da ação se for PLAYER_ACTION
  history_action: string | null;
  on_fail: number | null; // ID da próxima cena em caso de falha
  on_success: number | null; // ID da próxima cena em caso de sucesso
  on_hard_fail: number | null; // ID da próxima cena em caso de falha crítica
  scene: number; // ID da cena à qual esta ação pertence
}

export interface Scene {
  id: number;
  title: string;
  location: string;
  initial: boolean;
  description: string;
  act: number; // ID do Act
  order: number;
  // scene_actions: SceneAction[]; // REMOVIDO - Agora buscado sob demanda
  url: string;
}

export interface Act {
  id: number;
  title: string;
  description: string;
  reward_type: string;
  reward_id: number;
  // scenes: Scene[]; // REMOVIDO - Agora buscado sob demanda
}

export interface CharacterProgressOnAct {
  id: number;
  character: number; // ID do personagem
  act: Act; // Detalhes do Act (sem scenes aninhadas)
  current_scene: Scene; // Detalhes da cena atual (sem scene_actions aninhadas)
  finished: boolean;
  game_message?: string; // Adicionado para receber mensagens do backend
}

interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export async function fetchCharacters(): Promise<Character[]> {
  const response = await api.get<
    Character[] | PaginatedResponse<Character>
  >("/characters/");

  const data = response.data;

  if (Array.isArray(data)) {
    return data;
  }

  return data.results;
}

export async function fetchCharacter(
  characterId: number
): Promise<Character> {
  const response = await api.get<Character>(
    `/characters/${characterId}/`
  );

  return response.data;
}

export interface CreateCharacterPayload {
  name: string;
  gender: "male" | "female";
  age: number;
  level?: number;
  current_health?: number;
  max_health?: number;
}

export async function createCharacter(
  payload: CreateCharacterPayload
): Promise<Character> {
  const response = await api.post<Character>(
    "/characters/",
    payload
  );

  return response.data;
}

// Funções para o jogo
export async function fetchCharacterProgress(
  characterId: number
): Promise<CharacterProgressOnAct | null> {
  try {
    const response = await api.post<CharacterProgressOnAct>(
      "/scene_action_select/",
      { character_id: characterId }
    );
    return response.data;
  } catch (error) {
    console.error("Erro ao buscar ou iniciar progresso do personagem:", error);
    return null;
  }
}

export async function selectSceneAction(
  characterId: number,
  sceneActionId: number
): Promise<CharacterProgressOnAct> {
  const response = await api.post<CharacterProgressOnAct>(
    "/scene_action_select/",
    { character_id: characterId, scene_action_id: sceneActionId }
  );
  return response.data;
}

// NOVAS FUNÇÕES para buscar cenas e ações sob demanda
export async function fetchScene(sceneId: number): Promise<Scene> {
  const response = await api.get<Scene>(`/scenes/${sceneId}/`);
  return response.data;
}

export async function fetchSceneActionsForScene(sceneId: number): Promise<SceneAction[]> {
  // Assumindo que você tem um endpoint para listar SceneActions filtradas por scene_id
  // Ou você pode buscar todas e filtrar no frontend, mas um endpoint filtrado é melhor
  const response = await api.get<PaginatedResponse<SceneAction>>(`/scene_actions/?scene=${sceneId}`);
  return response.data.results;
}

export async function fetchAct(actId: number): Promise<Act> {
  const response = await api.get<Act>(`/acts/${actId}/`);
  return response.data;
}