# Baton

Bot Discord qui distribue le « bâton de la parole » : une commande slash rend muet ou rétablit un utilisateur cible dans un salon vocal, sans que celui-ci puisse se le donner lui-même.

## Fonctionnement

- `/baton` — bascule l'état du bâton : donne la parole à l'utilisateur cible (`mute=false`) ou la lui retire (`mute=true`).
- La commande est refusée si l'utilisateur cible tente de se l'auto-attribuer.
- Si l'utilisateur cible change de salon vocal, l'état est réappliqué.
- L'utilisateur cible est fixé par la variable d'environnement `TARGET_USER_ID`.

## Configuration

| Variable | Rôle |
|---|---|
| `DISCORD_TOKEN` | Token du bot |
| `TARGET_USER_ID` | ID Discord de l'utilisateur qui reçoit le bâton |

Le bot s'arrête au démarrage si l'une des deux variables manque.

## Lancer

```bash
uv sync
export DISCORD_TOKEN=... TARGET_USER_ID=...
uv run main.py
```

Ou avec Docker :

```bash
docker compose up -d
```

## Limites

- Un seul utilisateur cible, un seul serveur : aucune gestion multi-guilde.
- État en mémoire (`has_baton`), perdu au redémarrage.
- Pas de tests automatisés.
