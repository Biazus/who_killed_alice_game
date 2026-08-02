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
        const data = await fetchCharacters();
        setCharacters(data);
      } catch (error) {
        console.error("Erro ao carregar personagens:", error);
        setError("Não foi possível carregar os personagens.");
      } finally {
        setLoading(false);
      }
    }

    loadCharacters();
  }, []);

  return (
    <main className="characters-page">
      <div className="page-heading">
        <div>
          <span className="eyebrow">WHO KILLED ALICE</span>
          <h1>Personagens</h1>
          <p>
            Cada rosto esconde uma versão diferente da verdade.
          </p>
        </div>

        <span className="case-number">CASO Nº 001</span>
      </div>

      {loading && (
        <div className="state-message">
          Consultando os arquivos...
        </div>
      )}

      {error && (
        <div className="state-message state-message--error">
          {error}
        </div>
      )}

      {!loading && !error && characters.length === 0 && (
        <div className="state-message">
          Nenhum personagem foi encontrado.
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