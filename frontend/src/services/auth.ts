import axios from "axios";
import { clearToken, saveToken } from "../tokenStorage";

interface LoginPayload {
  username: string;
  password: string;
}

interface LoginResponse {
  token: string;
}

const API_URL = "http://localhost:8000/api";

export async function login(
  credentials: LoginPayload
): Promise<string> {
  const response = await axios.post<LoginResponse>(
    `${API_URL}/token/`,
    credentials
  );

  const token = response.data.token;

  saveToken(token);

  return token;
}

export function logout(): void {
  clearToken();
}