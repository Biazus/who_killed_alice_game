import { useState } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";

import CharactersList from "./CharactersList";
import CharacterDetail from "./CharacterDetail";
import LoginForm from "./LoginForm";
import { logout } from "./services/auth";
import { isAuthenticated } from "./tokenStorage";
import "./App.css";

function App() {
  const [authenticated, setAuthenticated] = useState(isAuthenticated());
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    setAuthenticated(false);
    navigate("/login");
  }

  if (!authenticated) {
    return (
      <div className="auth-page">
        <div className="auth-decoration auth-decoration--one" />
        <div className="auth-decoration auth-decoration--two" />

        <LoginForm
          onLoggedIn={() => {
            setAuthenticated(true);
            navigate("/characters", { replace: true });
          }}
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

        <button className="logout-button" onClick={handleLogout}>
          Encerrar sessão
        </button>
      </header>

      <Routes>
        <Route path="/" element={<CharactersList />} />{" "}
        {/* Rota padrão para a lista de personagens */}
        <Route path="/characters" element={<CharactersList />} />{" "}
        {/* Rota explícita para a lista */}
        <Route
          path="/characters/:id"
          element={<CharacterDetail />}
        />{" "}
      </Routes>
    </div>
  );
}

export default App;