



# Utiliser une image officielle Python avec la version 3.10
FROM python:3.10-slim

# Installer les outils de compilation
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers (code Flask, modèle, HTML)
COPY . .

# Exposer le port 8000
EXPOSE 8000

# Commande pour lancer l'application Flask
CMD ["python", "app.py"]


