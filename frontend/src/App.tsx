import { useState } from "react";
import { Routes, Route, useNavigate } from "react-router-dom"; // Importe Routes, Route e useNavigate

import CharactersList from "./CharactersList";
import CharacterDetail from "./CharacterDetail"; // Importe o novo componente
import LoginForm from "./LoginForm";
import { logout } from "./services/auth";
import { isAuthenticated } from "./tokenStorage";
import "./App.css";

function App() {
  const [authenticated, setAuthenticated] = useState(isAuthenticated());
  const navigate = useNavigate(); // Hook para navegação programática

  function handleLogout() {
    logout();
    setAuthenticated(false);
    navigate("/login"); // Redireciona para a tela de login após o logout
  }

  if (!authenticated) {
    return (
      <div className="auth-page">
        <div className="auth-decoration auth-decoration--one" />
        <div className="auth-decoration auth-decoration--two" />

        <LoginForm onLoggedIn={() => setAuthenticated(true)} />
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

      {/* Aqui definimos as rotas da aplicação */}
      <Routes>
        <Route path="/" element={<CharactersList />} />{" "}
        {/* Rota padrão para a lista de personagens */}
        <Route path="/characters" element={<CharactersList />} />{" "}
        {/* Rota explícita para a lista */}
        <Route
          path="/characters/:id"
          element={<CharacterDetail />}
        />{" "}
        {/* Nova rota para os detalhes do personagem */}
        <Route path="/login" element={<LoginForm onLoggedIn={() => setAuthenticated(true)} />} /> {/* Adicione uma rota para o login, caso precise ser acessado diretamente */}
      </Routes>
    </div>
  );
}

export default App;