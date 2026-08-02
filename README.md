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
  
**Resolution:**
compute a combined attribute value (e.g. weighted average),
subtract action difficulty to get a chance (0–100),
`roll 1–100` → `success if roll <= chance`.

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

**Install dependencies**

   `pip install -r requirements.txt`
   
**Apply migrations**

   `python manage.py migrate`
   
**Load initial data**
   - `python manage.py loaddata attributes.json`
   - `python manage.py loaddata actions.json`
   - `python manage.py loaddata item_types.json`
   - `python manage.py loaddata items.json`  
   - `python manage.py loaddata modifier_categories.json`
   - `python manage.py loaddata modifiers.json`
   - `python manage.py loaddata modifier_attribute_effects.json`
   - `python manage.py loaddata item_attribute_effects.json`
   
**Run the development server**

   `python manage.py runserver`
   
## Design Philosophy
**System‑first**: rigid, explicit mechanics; narrative is layered on top.

**On‑the‑fly computation**: attributes are not fully stored per character; they are derived from base + modifiers (+ items).

**Difficulty as tuning knob**: game difficulty can be globally adjusted by:
- raising/lowering the base attribute value, or
- changing action difficulties.

## TODOs (next few days)
### Tech:
- [ ] Black, isort, etc.
- [ ] Test suite

### Narrative
- [ ] Add items to success rate
- [ ] Block actions if player doesn't hold certain items
- [ ] Design on how to earn modifiers per game actions / luck
- [ ] Few adjustments on weights
- [ ] Add more attributes / modifier
  
This repository is the mechanical backbone of the story engine. Alice’s murderer may be hidden in the narrative, but this code decides whether you sneak past the warehouse guards, decode the ritual marks, or break under post‑apocalyptic horrors.
