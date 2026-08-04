# Who Killed Alice? – Game Backend
A narrative-focused tabletop-style RPG engine built with Django and Django REST Framework, set in a post‑apocalyptic world of vampires, druids, fae, and human survivors – all circling around the mystery: **Who killed Alice?**

This backend implements the core game mechanics:

## Features
### Characters & Modifiers

Characters are created with a set of random modifiers (perks & flaws).
Modifiers affect attributes via precomputed `CharacterModifierAttributeValue`.
### Attributes System

Rich attribute catalog (noise, stealth, social, investigation, resistance, faction reputation, territory knowledge, Alice case intuition, etc.).

Effective attribute value is calculated on the fly:
`base_value` (e.g. 75 or 80) + sum of modifier effects (+ item effects later).

### Actions & Checks

Action models describe in‑game actions (stealth, investigation, social, resistance, reputation).
For complex actions, multiple `ActionAttributeRequirement` entries define:
- which attributes matter,
- weights,
- per‑attribute difficulty adjustments.

### API Endpoints

Endpoints to:
- create characters,
- inspect their effective attributes,
- perform actions and receive full roll details (chance, roll, success/failure),
- and more (TODO)

## Tech Stack
**Backend**: Django 

**API**: Django REST Framework 

## Getting Started

   - `docker-compose build -d`
   - `docker-compose up -d`
   - `docker-compose exec web python manage.py createsuperuser`
   
**Load initial data**
   - `docker-compose exec web python manage.py load_all`

   
## Design Philosophy
**System‑first**: rigid, explicit mechanics; narrative is layered on top.

**On‑the‑fly computation**: attributes are not fully stored per character; they are derived from base + modifiers (+ items).

**Difficulty as tuning knob**: game difficulty can be globally adjusted by:
- raising/lowering the base attribute value, or
- changing action difficulties.

## TODOs (next few days)
### Tech:
- [ ] Test suite
- [ ] Document functions

### Narrative
- [ ] Block actions if player doesn't hold certain items
- [ ] Design on how to earn modifiers per game actions / luck
- [ ] Add more attributes / modifier
  
This repository is the mechanical backbone of the story engine. Alice’s murderer may be hidden in the narrative, but this code decides whether you sneak past the warehouse guards, decode the ritual marks, or break under post‑apocalyptic horrors.

<img width="652" height="907" alt="1" src="https://github.com/user-attachments/assets/7be0e194-3469-4cf2-9c67-588a0da9aac7" />
<img width="767" height="845" alt="2" src="https://github.com/user-attachments/assets/5b363352-3d76-44b4-976c-657b1f86e757" />

