import type { CSSProperties } from "react";
import { CircleHelp, UserRound, ArrowUpRight } from "lucide-react";
import { useNavigate } from "react-router-dom";

import type { Character } from "./services/characters";
import { modifierVisualMap } from "./modifierVisuals";

interface CharacterCardProps {
  character: Character;
}

type CharacterPalette = {
  accent: string;
  accentSoft: string;
  accentGlow: string;
  cardTint: string;
};

const characterPalettes: CharacterPalette[] = [
  {
    accent: "#ef5a4d",
    accentSoft: "rgba(239, 90, 77, 0.32)",
    accentGlow: "rgba(239, 90, 77, 0.34)",
    cardTint: "rgba(155, 42, 34, 0.20)",
  },
  {
    accent: "#d59a52",
    accentSoft: "rgba(213, 154, 82, 0.30)",
    accentGlow: "rgba(213, 154, 82, 0.30)",
    cardTint: "rgba(125, 77, 30, 0.20)",
  },
  {
    accent: "#66a99c",
    accentSoft: "rgba(102, 169, 156, 0.28)",
    accentGlow: "rgba(102, 169, 156, 0.28)",
    cardTint: "rgba(35, 105, 93, 0.20)",
  },
  {
    accent: "#7e9fc8",
    accentSoft: "rgba(126, 159, 200, 0.28)",
    accentGlow: "rgba(126, 159, 200, 0.28)",
    cardTint: "rgba(54, 82, 128, 0.22)",
  },
  {
    accent: "#a88ac4",
    accentSoft: "rgba(168, 138, 196, 0.28)",
    accentGlow: "rgba(168, 138, 196, 0.30)",
    cardTint: "rgba(99, 62, 123, 0.22)",
  },
  {
    accent: "#94ae73",
    accentSoft: "rgba(148, 174, 115, 0.28)",
    accentGlow: "rgba(148, 174, 115, 0.28)",
    cardTint: "rgba(73, 99, 42, 0.22)",
  },
];

function getCharacterPalette(characterId: number): CSSProperties {
  const palette =
    characterPalettes[characterId % characterPalettes.length];

  return {
    "--character-accent": palette.accent,
    "--character-accent-soft": palette.accentSoft,
    "--character-accent-glow": palette.accentGlow,
    "--character-card-tint": palette.cardTint,
  } as CSSProperties;
}

function decodeHtmlEntities(value: string): string {
  const textarea = document.createElement("textarea");
  textarea.innerHTML = value;

  return textarea.value;
}

function getInitials(name: string): string {
  return name
    .trim()
    .split(" ")
    .slice(0, 2)
    .map((part) => part.charAt(0))
    .join("")
    .toUpperCase();
}

function CharacterCard({ character }: CharacterCardProps) {
  const modifiers = character.modifiers ?? [];
  const navigate = useNavigate();

  function openCharacterDetail() {
    navigate(`/characters/${character.id}`);
  }

  const owner = character.owner
    ? `@${character.owner}`
    : "Desconhecido";

  return (
    <article
      className="character-card character-card--clickable"
      style={getCharacterPalette(character.id)}
      onClick={openCharacterDetail}
    >
      <div className="character-card__accent" />

      <header className="character-card__header">
        <div className="character-card__identity">
          <div
            className="character-portrait"
            aria-label={`Identidade visual de ${character.name}`}
          >
            <span>{getInitials(character.name)}</span>
          </div>

          <div className="character-card__name">
            <span className="eyebrow">SOBREVIVENTE REGISTRADO</span>

            <h2>{character.name}</h2>

            <span className="character-owner">
              <UserRound size={13} aria-hidden="true" />
              {owner}
            </span>
          </div>
        </div>

        <div className="character-level">
          <span>NÍVEL</span>
          <strong>{character.level}</strong>
        </div>
      </header>

      <div className="character-card__divider" />

      <section
        className="character-summary"
        aria-label="Resumo do personagem"
      >
        <div className="summary-item">
          <span className="summary-item__label">Registro</span>
          <strong>#{String(character.id).padStart(3, "0")}</strong>
        </div>

        <div className="summary-item">
          <span className="summary-item__label">Traços</span>
          <strong>{modifiers.length}</strong>
        </div>

        <div className="summary-item">
          <span className="summary-item__label">Status</span>
          <strong className="status-active">ATIVO</strong>
        </div>
      </section>

      <section
        className="modifiers-section"
        aria-labelledby={`modifiers-${character.id}`}
      >
        <div className="modifiers-section__heading">
          <div>
            <span className="eyebrow">
              EVIDÊNCIAS COMPORTAMENTAIS
            </span>

            <h3 id={`modifiers-${character.id}`}>
              Traços revelados
            </h3>
          </div>

          <span className="modifier-count">{modifiers.length}</span>
        </div>

        {modifiers.length > 0 ? (
          <div className="modifier-grid">
            {modifiers.map((item) => {
              const category = decodeHtmlEntities(
                item.modifier.category
              );

              const visual = modifierVisualMap[item.modifier.name];

              const Icon = visual?.icon ?? CircleHelp;

              const tooltipId = `modifier-description-${item.id}`;

              return (
                <article
                  className="modifier-tile"
                  key={item.id}
                  tabIndex={0}
                  aria-describedby={tooltipId}
                  onClick={(event) => event.stopPropagation()}
                >
                  <div className="modifier-tile__icon">
                    <Icon
                      size={22} /* Ajustado para 22px */
                      strokeWidth={1.7}
                      className={visual?.iconClassName}
                      aria-hidden="true"
                    />
                  </div>

                  <span className="modifier-tile__category">
                    {category}
                  </span>

                  <h4>{item.modifier.name}</h4>

                  <div
                    className="modifier-tooltip"
                    id={tooltipId}
                    role="tooltip"
                  >
                    <span className="modifier-tooltip__label">
                      {item.modifier.name}
                    </span>

                    <p>{item.modifier.description}</p>
                  </div>
                </article>
              );
            })}
          </div>
        ) : (
          <p className="modifier-empty">
            Nenhum traço foi identificado neste arquivo.
          </p>
        )}
      </section>

      <footer className="character-card__footer">
        <span>ARQUIVO CONFIDENCIAL · CASO Nº 001</span>
        <button
          type="button"
          className="character-card__open"
          onClick={(event) => {
            event.stopPropagation();
            openCharacterDetail();
          }}
        >
          Abrir dossiê
          <ArrowUpRight size={14} aria-hidden="true" /> {/* Ajustado para 14px */}
        </button>
      </footer>
    </article>
  );
}

export default CharacterCard;