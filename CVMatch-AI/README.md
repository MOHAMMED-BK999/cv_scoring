# CVMatch-AI — Solution Intelligente de Recrutement 🚀

**CVMatch-AI** est une application professionnelle conçue pour les recruteurs. Elle utilise l'Intelligence Artificielle pour analyser, comprendre et évaluer automatiquement les CV des candidats. Son objectif est d'automatiser et d'accélérer le processus de recrutement en fournissant des scores de correspondance précis et des insights détaillés.

---

## ✨ Fonctionnalités Principales

*   **Analyse Automatique des CV** : Lisez et analysez les fichiers PDF et DOCX sans effort.
*   **Extraction de Données Intelligente** : Récupérez les compétences, l'expérience, les diplômes et les informations de contact.
*   **Correspondance (Matching) Précise** : Comparez le profil du candidat avec l'offre d'emploi pour obtenir un score de compatibilité.
*   **Tableau de Bord Visuel** : Visualisez les résultats avec des graphiques clairs et interactifs.
*   **Interface Multilingue** : Application disponible en plusieurs langues (grâce au système i18n).
*   **API RESTful** : Backend robuste et scalable pour toutes les opérations.

---

## 📊 Méthodologie du Projet

Le système fonctionne en plusieurs étapes claires :

```
📄 Document  →  📝 Texte  →  📋 Données  →  📐 Vecteurs  →  🏆 Score
  (Input)      (Parsing)    (Extraction)   (Embeddings)   (Matching)
```

### Architecture

- **Frontend** : Application React 19 avec TypeScript et Vite
- **Backend** : API FastAPI avec Python 3.11+
- **Base de Données** : PostgreSQL avec pgvector pour les embeddings
- **IA** : Gemini API et Ollama (mode local optionnel)
- **Services** : Firebase pour l'authentification et la persistance

---

## 💻 Stack Technologique

### Frontend (50.3% du code)
*   **React 19** & **TypeScript** - Interface utilisateur type-safe et moderne
*   **Vite** - Build tool ultra-rapide
*   **Tailwind CSS** - Design responsive et moderne
*   **Recharts** - Visualisations graphiques interactives
*   **Axios** - Client HTTP pour communiquer avec le backend
*   **Firebase** - Authentification utilisateur

### Backend (48.8% du code)
*   **FastAPI** & **Uvicorn** - Framework API haute performance
*   **PostgreSQL** avec **pgvector** - Base de données vectorielle (Neon)
*   **SQLAlchemy** & **Alembic** - ORM et migrations
*   **Pydantic** - Validation de données
*   **Python-jose & Passlib** - Authentification sécurisée

### IA et Traitement (NLP)
*   **Gemini API** - Modèle d'IA principal pour l'extraction et l'évaluation
*   **Ollama** - Support optionnel pour les modèles locaux (llama3, Qwen)
*   **ChromaDB** - Alternative pour la gestion des vecteurs (tests locaux)
*   **BAAI Embeddings** - Modèles d'embeddings performants

### DevOps
*   **Docker & Docker Compose** - Containerisation et orchestration
*   **PostgreSQL pgvector** - Support des vecteurs en base de données

---

## 🚀 Guide de Démarrage

### Prérequis
- Python 3.11+
- Node.js 18+
- PostgreSQL avec extension pgvector (ou Docker)
- Clés API Gemini (optionnel pour Ollama local)

### Installation Rapide avec Docker

```bash
# À la racine du projet
docker-compose up -d
```

Cela démarre :
- PostgreSQL (port 5432)
- ChromaDB (port 8001)

### Installation Manuelle

**1. Configuration des variables d'environnement**

Créez un fichier `.env` à la racine ou dans le dossier `backend` :

```env
# Frontend
VITE_API_BASE_URL=http://127.0.0.1:8000

# Backend
APP_NAME=PFE CV Scoring API
APP_ENV=development
API_PREFIX=/api/v1

# IA (Gemini)
GEMINI_API_KEY=your_gemini_key_here

# Firebase (optionnel)
FIREBASE_PROJECT_ID=cv-scoring-8aae1
FIREBASE_API_KEY=your_firebase_key_here

# Ollama local (optionnel)
# OLLAMA_ENABLED=true
# OLLAMA_BASE_URL=http://127.0.0.1:11434
# OLLAMA_MODEL=llama3.1:8b
```

**2. Backend (FastAPI)**

```bash
cd CVMatch-AI/backend
python -m venv .venv
source .venv/bin/activate  # Windows: .\venv\Scripts\Activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

L'API sera disponible sur `http://127.0.0.1:8000`
Documentation Swagger : `http://127.0.0.1:8000/docs`

**3. Frontend (React)**

```bash
cd CVMatch-AI/frontend
npm install
npm run dev
```

L'application sera disponible sur `http://localhost:5173`

---

## 📁 Structure du Projet

```
CVMatch-AI/
├── frontend/                 # Application React
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
├── backend/                  # API FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── database/
│   ├── migrations/           # Alembic
│   ├── requirements.txt
│   └── .env
├── docker-compose.yml        # Services (PostgreSQL, ChromaDB)
├── package.json              # Workspace scripts
└── README.md
```

---

## 🔧 Scripts Disponibles

```bash
# Frontend
npm run frontend:dev     # Démarrer le serveur de développement
npm run frontend:build   # Compiler pour la production

# Backend
npm run backend:dev      # Démarrer le backend en mode dev
npm run backend:test     # Exécuter les tests
```

---


## 📈 Déploiement

### Option 1 : Docker
```bash
docker-compose up --build
```

### Option 2 : Kaggle
Consultez `KAGGLE_BACKEND.md` pour les instructions de déploiement sur Kaggle.

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Merci de :
1. Créer une branche pour votre fonctionnalité (`git checkout -b feature/NomFeature`)
2. Commiter vos modifications (`git commit -m 'Ajouter NomFeature'`)
3. Pousser vers la branche (`git push origin feature/NomFeature`)
4. Ouvrir une Pull Request

---

## 📝 Licence

Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus de détails.

---

## 📧 Support

Pour toute question ou problème, n'hésitez pas à ouvrir une issue sur GitHub ou contacter l'équipe de développement.

**Dernière mise à jour** : Juin 2026
