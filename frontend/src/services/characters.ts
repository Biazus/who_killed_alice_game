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