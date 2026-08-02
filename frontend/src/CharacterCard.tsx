import type { Character } from "./services/characters";

interface CharacterCardProps {
  character: Character;
}

function decodeHtmlEntities(value: string): string {
  const textarea = document.createElement("textarea");
  textarea.innerHTML = value;
  return textarea.value;
}

function CharacterCard({ character }: CharacterCardProps) {
  return (
    <article className="character-card">
      <div className="character-card__top">
        <div>
          <span className="eyebrow">ARQUIVO DE PERSONAGEM</span>
          <h2>{character.name}</h2>
        </div>

        <span className="level-badge">
          Nv. {character.level}
        </span>
      </div>

      <div className="character-card__divider" />

      <div className="character-meta">
        <div>
          <span className="meta-label">Proprietário</span>
          <strong>@{character.owner}</strong>
        </div>

        <div>
          <span className="meta-label">Modificadores</span>
          <strong>{character.modifiers?.length ?? 0}</strong>
        </div>
      </div>

      <section className="modifiers-section">
        <div className="section-heading">
          <span className="section-mark" />
          <h3>Traços revelados</h3>
        </div>

        <div className="modifier-list">
          {character.modifiers?.map((item) => (
            <div className="modifier-card" key={item.id}>
              <span className="modifier-card__category">
                {decodeHtmlEntities(item.modifier.category)}
              </span>

              <h4>{item.modifier.name}</h4>

              <p>{item.modifier.description}</p>
            </div>
          ))}
        </div>
      </section>
    </article>
  );
}

export default CharacterCard;