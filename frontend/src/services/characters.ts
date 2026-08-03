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
}

export interface Scene {
  id: number;
  title: string;
  location: string;
  initial: boolean;
  description: string;
  act: number; // ID do Act
  order: number;
  scene_actions: SceneAction[]; // Ações disponíveis nesta cena
  url: string;
}

export interface Act {
  id: number;
  title: string;
  description: string;
  reward_type: string;
  reward_id: number;
  scenes: Scene[]; // Cenas dentro deste ato
}

export interface CharacterProgressOnAct {
  id: number;
  character: number; // ID do personagem
  act: Act; // Detalhes do Act
  current_scene: Scene; // Detalhes da cena atual
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

// Novas funções para o jogo
export async function fetchCharacterProgress(
  characterId: number
): Promise<CharacterProgressOnAct | null> {
  try {
    // Agora, a primeira chamada para /scene_action_select sem scene_action_id
    // fará com que o backend crie o progresso se ele não existir.
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