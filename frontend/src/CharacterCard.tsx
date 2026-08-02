import type { ComponentType } from "react";
import {
  Brain,
  CircleHelp,
  Eye,
  Footprints,
  Handshake,
  HeartPulse,
  MessageCircle,
  Search,
  Shield,
  UserRound,
  type LucideProps,
} from "lucide-react";
import type { Character } from "./services/characters";

interface CharacterCardProps {
  character: Character;
}

type ModifierIcon = ComponentType<LucideProps>;

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

function getModifierIcon(
  name: string,
  category: string
): ModifierIcon {
  const normalizedName = name.toLowerCase();
  const normalizedCategory = category.toLowerCase();

  if (
    normalizedName.includes("coração") ||
    normalizedCategory.includes("resistência") ||
    normalizedCategory.includes("sobrevivência")
  ) {
    return HeartPulse;
  }

  if (
    normalizedName.includes("rosto") ||
    normalizedCategory.includes("persuasão") ||
    normalizedCategory.includes("interação social")
  ) {
    return MessageCircle;
  }

  if (
    normalizedName.includes("chão") ||
    normalizedName.includes("passagem") ||
    normalizedCategory.includes("investigação")
  ) {
    return Footprints;
  }

  if (normalizedCategory.includes("observação")) {
    return Eye;
  }

  if (normalizedCategory.includes("proteção")) {
    return Shield;
  }

  if (normalizedCategory.includes("inteligência")) {
    return Brain;
  }

  if (normalizedCategory.includes("social")) {
    return Handshake;
  }

  if (normalizedCategory.includes("busca")) {
    return Search;
  }

  return CircleHelp;
}

function CharacterCard({ character }: CharacterCardProps) {
  const modifiers = character.modifiers ?? [];
  const owner = character.owner
    ? `@${character.owner}`
    : "Desconhecido";

  return (
    <article className="character-card">
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

      <section className="character-summary" aria-label="Resumo do personagem">
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
            <span className="eyebrow">EVIDÊNCIAS COMPORTAMENTAIS</span>
            <h3 id={`modifiers-${character.id}`}>
              Traços revelados
            </h3>
          </div>

          <span className="modifier-count">
            {modifiers.length}
          </span>
        </div>

        {modifiers.length > 0 ? (
          <div className="modifier-grid">
            {modifiers.map((item) => {
              const category = decodeHtmlEntities(
                item.modifier.category
              );

              const Icon = getModifierIcon(
                item.modifier.name,
                category
              );

              const tooltipId = `modifier-description-${item.id}`;

              return (
                <article
                  className="modifier-tile"
                  key={item.id}
                  tabIndex={0}
                  aria-describedby={tooltipId}
                >
                  <div className="modifier-tile__icon">
                    <Icon
                      size={27}
                      strokeWidth={1.7}
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
        <span>ARQUIVO CONFIDENCIAL</span>
        <span>CASO Nº 001</span>
      </footer>
    </article>
  );
}

export default CharacterCard;