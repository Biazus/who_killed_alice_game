import { useEffect, useState } from "react";
import {
  fetchCharacters,
  type Character,
} from "./services/characters";
import CharacterCard from "./CharacterCard";

function CharactersList() {
  const [characters, setCharacters] = useState<Character[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadCharacters() {
      try {
        setLoading(true);
        setError(null);

        const data = await fetchCharacters();
        setCharacters(data);
      } catch (error) {
        console.error("Erro ao carregar personagens:", error);
        setError(
          "Os arquivos foram comprometidos. Não foi possível carregar os personagens."
        );
      } finally {
        setLoading(false);
      }
    }

    loadCharacters();
  }, []);

  return (
    <main className="characters-page">
      <section className="case-hero">
        <div className="case-hero__content">
          <span className="eyebrow">ARQUIVOS DO CASO · ACESSO RESTRITO</span>

          <h1>
            Quem matou
            <span>Alice?</span>
          </h1>

          <p>
            Todo sobrevivente guarda uma versão da noite em que Alice
            desapareceu. Examine os traços, confronte as evidências e
            encontre as contradições.
          </p>
        </div>

        <aside className="case-stamp" aria-label="Informações do caso">
          <span>INVESTIGAÇÃO ATIVA</span>
          <strong>CASO Nº 001</strong>
          <small>
            {loading
              ? "Consultando registros"
              : `${characters.length} registro${characters.length === 1 ? "" : "s"}`}
          </small>
        </aside>
      </section>

      <div className="section-title">
        <div>
          <span className="eyebrow">BANCO DE DADOS</span>
          <h2>Personagens registrados</h2>
        </div>

        <div className="section-title__line" />
      </div>

      {loading && (
        <div className="state-message state-message--loading">
          <span className="loading-mark" />
          Consultando os arquivos confidenciais...
        </div>
      )}

      {error && (
        <div className="state-message state-message--error">
          <strong>Falha na consulta</strong>
          <span>{error}</span>
        </div>
      )}

      {!loading && !error && characters.length === 0 && (
        <div className="state-message">
          Nenhum personagem foi encontrado neste arquivo.
        </div>
      )}

      {!loading && !error && characters.length > 0 && (
        <div className="characters-grid">
          {characters.map((character) => (
            <CharacterCard
              key={character.id}
              character={character}
            />
          ))}
        </div>
      )}
    </main>
  );
}

export default CharactersList;