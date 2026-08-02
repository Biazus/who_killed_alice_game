import { useState } from "react";
import CharactersList from "./CharactersList";
import LoginForm from "./LoginForm";
import { logout } from "./services/auth";
import { isAuthenticated } from "./tokenStorage";
import "./App.css";

function App() {
  const [authenticated, setAuthenticated] = useState(
    isAuthenticated()
  );

  function handleLogout() {
    logout();
    setAuthenticated(false);
  }

  if (!authenticated) {
    return (
      <div className="auth-page">
        <div className="auth-decoration auth-decoration--one" />
        <div className="auth-decoration auth-decoration--two" />

        <LoginForm
          onLoggedIn={() => setAuthenticated(true)}
        />
      </div>
    );
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <span className="brand__symbol">✦</span>
          <span>WHO KILLED ALICE</span>
        </div>

        <button
          className="logout-button"
          onClick={handleLogout}
        >
          Encerrar sessão
        </button>
      </header>

      <CharactersList />
    </div>
  );
}

export default App;