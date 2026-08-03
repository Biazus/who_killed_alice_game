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