FROM python:3.11-slim

WORKDIR /app

# Installation de la bibliothèque requise sans cache pour alléger l'image
RUN pip install --no-cache-dir discord.py

# Copie du script dans le conteneur
COPY main.py .

# Commande d'exécution
CMD ["python", "main.py"]
