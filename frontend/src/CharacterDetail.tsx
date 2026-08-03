// CharacterDetail.tsx
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  ArrowLeft,
  Backpack,
  CircleHelp,
  HeartPulse,
  Shield,
  UserRound,
  Dice5,
  Percent,
} from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";

import {
  fetchCharacter,
  fetchCharacterProgress,
  selectSceneAction,
  fetchSceneActionsForScene,
  type Character,
  type InventoryItem,
  type CharacterProgressOnAct,
  type SceneAction,
  type Scene,
  type Act,
} from "./services/characters";
import { modifierVisualMap } from "./modifierVisuals";

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

// Função para determinar a cor de fundo da dificuldade (mais claro a mais avermelhado)
function getDifficultyBackgroundColor(difficulty: number): string {
  // Escala de cores para dificuldade (exemplo: de um vermelho claro a um vermelho escuro)
  // Você pode ajustar esses valores RGB para a paleta exata que deseja!
  if (difficulty === 1) return "rgba(255, 220, 220, 0.8)"; // Vermelho muito claro
  if (difficulty === 2) return "rgba(255, 180, 180, 0.8)"; // Vermelho claro
  if (difficulty === 3) return "rgba(255, 140, 140, 0.8)"; // Vermelho médio
  if (difficulty === 4) return "rgba(255, 100, 100, 0.8)"; // Vermelho mais escuro
  if (difficulty >= 5) return "rgba(255, 60, 60, 0.8)";   // Vermelho intenso
  return "rgba(200, 200, 200, 0.8)"; // Cor padrão para casos não mapeados
}

function CharacterDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [character, setCharacter] = useState<Character | null>(null);
  const [characterProgress, setCharacterProgress] =
    useState<CharacterProgressOnAct | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSceneAction, setSelectedSceneAction] =
    useState<SceneAction | null>(null);
  const [isSubmittingAction, setIsSubmittingAction] = useState(false);
  const [gameMessage, setGameMessage] = useState<string | null>(null);
  const [currentSceneActions, setCurrentSceneActions] = useState<SceneAction[]>([]);

  const characterId = useMemo(() => Number(id), [id]);

  const inventoryItems = useMemo<InventoryItem[]>(() => {
    return character?.inventory?.flatMap((inventory) => inventory.items) ?? [];
  }, [character]);

  const loadCharacterAndProgress = useCallback(async () => {
    if (!Number.isInteger(characterId) || characterId <= 0) {
      setError("O registro solicitado é inválido.");
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setGameMessage(null);
      setSelectedSceneAction(null);

      const charData = await fetchCharacter(characterId);
      setCharacter(charData);

      const progressData = await fetchCharacterProgress(characterId);
      setCharacterProgress(progressData);

      if (progressData && progressData.current_scene) {
        const actions = await fetchSceneActionsForScene(progressData.current_scene.id);
        setCurrentSceneActions(actions.filter(sa => sa.action_type === "P"));

        if (progressData.game_message) {
          setGameMessage(progressData.game_message);
        }
      } else {
        setGameMessage("Nenhum progresso encontrado. Iniciando nova aventura...");
      }
    } catch (requestError: any) {
      console.error("Erro ao carregar personagem ou progresso:", requestError);

      const errorMessage =
        requestError.response?.data?.detail ||
        "Não foi possível recuperar este dossiê nos arquivos da investigação.";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [characterId]);

  useEffect(() => {
    loadCharacterAndProgress();
  }, [loadCharacterAndProgress]);

  useEffect(() => {
    async function loadSceneActions() {
      if (characterProgress && characterProgress.current_scene && !characterProgress.finished) {
        try {
          const actions = await fetchSceneActionsForScene(characterProgress.current_scene.id);
          setCurrentSceneActions(actions.filter(sa => sa.action_type === "P"));
        } catch (err) {
          console.error("Erro ao carregar ações da cena:", err);
          setCurrentSceneActions([]);
        }
      } else {
        setCurrentSceneActions([]);
      }
    }
    loadSceneActions();
  }, [characterProgress?.current_scene, characterProgress?.finished]);

  const handleSelectAction = (action: SceneAction) => {
    setSelectedSceneAction(action);
    setGameMessage(null);
  };

  const handleSubmitAction = async () => {
    if (!selectedSceneAction || !characterProgress) return;

    setIsSubmittingAction(true);
    setGameMessage("Rolando o dado...");

    try {
      const updatedProgress = await selectSceneAction(
        characterId,
        selectedSceneAction.id
      );
      setCharacterProgress(updatedProgress);
      setSelectedSceneAction(null);

      if (updatedProgress.game_message) {
        setGameMessage(updatedProgress.game_message);
      } else {
        setGameMessage("Ação realizada! Avançando para a próxima cena...");
      }

      if (updatedProgress.finished) {
        setGameMessage(updatedProgress.game_message || "O jogo chegou ao fim!");
      }

    } catch (submitError: any) {
      console.error("Erro ao submeter ação:", submitError);
      const errorMessage =
        submitError.response?.data?.detail ||
        "Falha ao realizar a ação. Tente novamente.";
      setGameMessage(`Erro: ${errorMessage}`);
    } finally {
      setIsSubmittingAction(false);
    }
  };

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

  const owner = character.owner ? `@${character.owner}` : "Desconhecido";

  const healthLabel =
    typeof character.current_health === "number" &&
    typeof character.max_health === "number"
      ? `${character.current_health} / ${character.max_health}`
      : "Não informado";

  const currentAct = characterProgress?.act;
  const currentScene = characterProgress?.current_scene;
  const availableSceneActions = currentSceneActions;

  // Determina se a rolagem foi um sucesso ou falha para o card
  const rollSuccess = characterProgress?.roll_success;

  return (
    <main className="character-detail-page">
      <div className="detail-header-act">
        <span className="eyebrow">ATO ATUAL</span>
        <h2>{currentAct?.title}</h2>
        <p>{currentAct?.description}</p>
      </div>

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

              <div className="detail-level">
                <span>Nível</span>
                <strong>{character.level}</strong>
              </div>
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
              <div className="detail-modifier-grid">
                {character.modifiers.map((entry) => {
                  const Icon =
                    modifierVisualMap[entry.modifier.name]?.icon ?? CircleHelp;

                  return (
                    <article
                      className="detail-modifier-card"
                      key={entry.id}
                    >
                      <Icon size={21} aria-hidden="true" />
                      {/* Ajuste aqui para que o nome do traço caiba */}
                      <h4 className="modifier-name-full">{entry.modifier.name}</h4>
                      <div className="modifier-tooltip">
                        <span className="modifier-tooltip__label">Descrição</span>
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
              <div className="detail-inventory-grid">
                {inventoryItems.map((item) => (
                  <article className="detail-inventory-card" key={item.id}>
                    <Backpack size={21} aria-hidden="true" />
                    <h4>{item.name}</h4>
                    <div className="inventory-tooltip">
                      <span className="inventory-tooltip__label">Detalhes</span>
                      <p>{item.description}</p>
                      <small>{formatWeight(item.weight)}</small>
                    </div>
                  </article>
                ))}
              </div>
            ) : (
              <p className="detail-empty">
                Nenhum item foi encontrado no inventário deste personagem.
              </p>
            )}
          </section>
        </section>

        <aside className="character-game-panel" aria-label="Área do Jogo">
          {characterProgress ? (
            <div className="game-content">
              <div className="game-scene">
                <span className="eyebrow">CENA ATUAL</span>
                <h3>{currentScene?.title}</h3>
                <p>{currentScene?.description}</p>
              </div>

              {gameMessage && (
                <div className="game-message-container">
                  <div className="game-message">{gameMessage}</div>
                  {/* Cards de Roll e Chance lado a lado */}
                  <div className="game-results-row">
                    {(characterProgress.roll_value !== undefined && characterProgress.roll_value !== null) && (
                      <div className={`game-result-card game-roll-card ${rollSuccess ? 'success' : 'failure'}`}>
                        <Dice5 size={24} aria-hidden="true" />
                        <strong>{characterProgress.roll_value}</strong>
                      </div>
                    )}
                    {(characterProgress.chance_value !== undefined && characterProgress.chance_value !== null) && (
                      <div className="game-result-card game-chance-card">
                        <Percent size={24} aria-hidden="true" />
                        <strong>{characterProgress.chance_value}%</strong>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {characterProgress.finished ? (
                <p className="game-empty">
                  O jogo para este personagem foi finalizado.
                  <br />
                  {gameMessage && <span>{gameMessage}</span>}
                </p>
              ) : (
                availableSceneActions.length > 0 ? (
                  <div className="game-actions">
                    <h4>O que você faz?</h4>
                    {availableSceneActions.map((sa) => (
                      <button
                        key={sa.id}
                        className={`game-action-button ${
                          selectedSceneAction?.id === sa.id ? "selected" : ""
                        }`}
                        onClick={() => handleSelectAction(sa)}
                        disabled={isSubmittingAction}
                        // Aplica a cor de fundo personalizada com base na dificuldade
                        style={{
                          backgroundColor: sa.action?.difficulty
                            ? getDifficultyBackgroundColor(sa.action.difficulty)
                            : undefined,
                        }}
                      >
                        {sa.description}
                        {/* Removido o span de dificuldade, pois a cor já indica */}
                      </button>
                    ))}
                    <button
                      className="game-submit-button"
                      onClick={handleSubmitAction}
                      disabled={!selectedSceneAction || isSubmittingAction}
                    >
                      <Dice5 size={18} aria-hidden="true" />
                      {isSubmittingAction ? "Rolando..." : "Rolar o Dado"}
                    </button>
                  </div>
                ) : (
                  <p className="game-empty">
                    Nenhuma ação disponível nesta cena.
                    <span>Aguardando o próximo movimento da história...</span>
                  </p>
                )
              )}
            </div>
          ) : (
            <div className="game-empty">
              <span>Carregando progresso do jogo...</span>
              {error && <p className="game-error">{error}</p>}
            </div>
          )}
        </aside>
      </div>
    </main>
  );
}

export default CharacterDetail;