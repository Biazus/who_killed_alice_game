import { useEffect, useMemo, useState } from "react";
import {
  ArrowLeft,
  Backpack,
  CircleHelp,
  HeartPulse,
  Shield,
  UserRound,
} from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";

import {
  fetchCharacter,
  type Character,
  type InventoryItem,
} from "./services/characters";
import { modifierVisualMap } from "./modifierVisuals"; // Certifique-se de que este import está correto

function decodeHtmlEntities(value: string): string {
  const textarea = document.createElement("textarea");
  textarea.innerHTML = value;

  return textarea.value;
}

function formatWeight(weight?: number): string {
  if (typeof weight !== "number") {
    return "Peso não informado";
  }

  return `${weight.toLocaleString("pt-BR")} kg`;
}

function CharacterDetail() {
  const { id } = useParams(); // Obtém o ID da URL
  const navigate = useNavigate();

  const [character, setCharacter] = useState<Character | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const inventoryItems = useMemo<InventoryItem[]>(() => {
    return character?.inventory?.flatMap((inventory) => inventory.items) ?? [];
  }, [character]);

  useEffect(() => {
    async function loadCharacter() {
      const characterId = Number(id);

      if (!Number.isInteger(characterId) || characterId <= 0) {
        setError("O registro solicitado é inválido.");
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);

        const data = await fetchCharacter(characterId);
        setCharacter(data);
      } catch (requestError) {
        console.error("Erro ao carregar personagem:", requestError);

        setError(
          "Não foi possível recuperar este dossiê nos arquivos da investigação."
        );
      } finally {
        setLoading(false);
      }
    }

    loadCharacter();
  }, [id]);

  if (loading) {
    return (
      <main className="character-detail-page">
        <div className="state-message state-message--loading">
          <span className="loading-mark" />
          Recuperando dossiê confidencial...
        </div>
      </main>
    );
  }

  if (error || !character) {
    return (
      <main className="character-detail-page">
        <div className="state-message state-message--error">
          <strong>Arquivo indisponível</strong>
          <span>{error ?? "Personagem não encontrado."}</span>

          <button
            type="button"
            className="detail-back-button"
            onClick={() => navigate("/characters")}
          >
            <ArrowLeft size={16} aria-hidden="true" />
            Voltar aos personagens
          </button>
        </div>
      </main>
    );
  }

  const owner = character.owner
    ? `@${character.owner}`
    : "Desconhecido";

  const healthLabel =
    typeof character.current_health === "number" &&
    typeof character.max_health === "number"
      ? `${character.current_health} / ${character.max_health}`
      : "Não informado";

  return (
    <main className="character-detail-page">
      <div className="character-detail-layout">
        <section className="character-detail-panel">
          <button
            type="button"
            className="detail-back-button"
            onClick={() => navigate("/characters")}
          >
            <ArrowLeft size={16} aria-hidden="true" />
            Voltar aos personagens
          </button>

          <header className="detail-header">
            <span className="eyebrow">
              DOSSIÊ DO SOBREVIVENTE · REGISTRO #
              {String(character.id).padStart(3, "0")}
            </span>

            <div className="detail-header__title">
              <div>
                <h1>{character.name}</h1>

                <span className="detail-owner">
                  <UserRound size={15} aria-hidden="true" />
                  {owner}
                </span>
              </div>

              <span className="detail-level">
                Nível <strong>{character.level}</strong>
              </span>
            </div>
          </header>

          <section className="detail-stats" aria-label="Dados do personagem">
            <div>
              <span>Saúde</span>
              <strong>
                <HeartPulse size={16} aria-hidden="true" />
                {healthLabel}
              </strong>
            </div>

            <div>
              <span>Idade</span>
              <strong>{character.age ?? "Não informada"}</strong>
            </div>

            <div>
              <span>Identidade</span>
              <strong>{character.gender ?? "Não informada"}</strong>
            </div>
          </section>

          <section className="detail-section">
            <div className="detail-section__heading">
              <div>
                <span className="eyebrow">PERFIL IDENTIFICADO</span>
                <h2>Traços revelados</h2>
              </div>

              <span className="detail-counter">
                {character.modifiers?.length ?? 0}
              </span>
            </div>

            {character.modifiers?.length ? (
              <div className="detail-modifier-list">
                {character.modifiers.map((entry) => {
                  const Icon =
                    modifierVisualMap[entry.modifier.name]?.icon ?? CircleHelp;

                  return (
                    <article
                      className="detail-modifier"
                      key={entry.id}
                    >
                      <Icon size={21} aria-hidden="true" />

                      <div>
                        <span>
                          {decodeHtmlEntities(entry.modifier.category)}
                        </span>

                        <h3>{entry.modifier.name}</h3>

                        <p>{entry.modifier.description}</p>
                      </div>
                    </article>
                  );
                })}
              </div>
            ) : (
              <p className="detail-empty">
                Nenhum traço foi identificado neste arquivo.
              </p>
            )}
          </section>

          <section className="detail-section">
            <div className="detail-section__heading">
              <div>
                <span className="eyebrow">EQUIPAMENTO RECUPERADO</span>
                <h2>Inventário</h2>
              </div>

              <span className="detail-counter">
                {inventoryItems.length}
              </span>
            </div>

            {inventoryItems.length > 0 ? (
              <div className="inventory-list">
                {inventoryItems.map((item) => (
                  <details className="inventory-item" key={item.id}>
                    <summary>
                      <span className="inventory-item__icon">
                        <Backpack size={18} aria-hidden="true" />
                      </span>

                      <span className="inventory-item__title">
                        <strong>{item.name}</strong>
                        <small>{formatWeight(item.weight)}</small>
                      </span>

                      <span className="inventory-item__reveal">
                        Detalhes
                      </span>
                    </summary>

                    <div className="inventory-item__content">
                      <p>{item.description}</p>

                      <span>
                        <Shield size={14} aria-hidden="true" />
                        Item #{String(item.id).padStart(3, "0")}
                      </span>
                    </div>
                  </details>
                ))}
              </div>
            ) : (
              <p className="detail-empty">
                Nenhum item foi encontrado no inventário deste personagem.
              </p>
            )}
          </section>
        </section>

        <aside
          className="character-game-placeholder"
          aria-label="Área reservada para o jogo"
        >
          <span>Área reservada para a experiência do jogo</span>
        </aside>
      </div>
    </main>
  );
}

export default CharacterDetail;