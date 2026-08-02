import { FormEvent, useState } from "react";
import { login } from "./services/auth";

interface LoginFormProps {
  onLoggedIn: () => void;
}

function LoginForm({ onLoggedIn }: LoginFormProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    setLoading(true);
    setError(null);

    try {
      await login({
        username,
        password,
      });

      onLoggedIn();
    } catch (error: unknown) {
      console.error("Erro ao fazer login:", error);
      setError("Usuário ou senha inválidos.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="login-card" onSubmit={handleSubmit}>
      <div className="login-card__mark">✦</div>

      <span className="eyebrow">ACESSO RESTRITO</span>

      <h1>Entre no arquivo</h1>

      <p className="login-card__description">
        As respostas estão escondidas entre os sobreviventes.
      </p>

      <div className="form-field">
        <label htmlFor="username">Usuário</label>

        <input
          id="username"
          value={username}
          onChange={(event) =>
            setUsername(event.target.value)
          }
          autoComplete="username"
          required
        />
      </div>

      <div className="form-field">
        <label htmlFor="password">Senha</label>

        <input
          id="password"
          type="password"
          value={password}
          onChange={(event) =>
            setPassword(event.target.value)
          }
          autoComplete="current-password"
          required
        />
      </div>

      {error && (
        <p className="form-error">
          {error}
        </p>
      )}

      <button
        className="primary-button"
        type="submit"
        disabled={loading}
      >
        {loading ? "Verificando..." : "Acessar arquivos"}
      </button>
    </form>
  );
}

export default LoginForm;