# CVMatch-AI — Solution Intelligente de Recrutement 🚀

**CVMatch-AI** est une application professionnelle conçue pour les recruteurs. Elle utilise l'Intelligence Artificielle pour analyser, comprendre et évaluer automatiquement les CV des candidats. Son but est de trouver le meilleur candidat pour une offre d'emploi spécifique grâce à des modèles de langage naturel (NLP) très avancés.

---

## ✨ Fonctionnalités Principales

*   **Analyse Automatique des CV** : Lisez les fichiers PDF et DOCX sans effort.
*   **Extraction de Données Intelligente** : Récupérez les compétences, l'expérience, les diplômes et les informations de contact.
*   **Correspondance (Matching) Précise** : Comparez le profil du candidat avec l'offre d'emploi pour obtenir un score de compatibilité.
*   **Tableau de Bord Visuel** : Visualisez les résultats avec des graphiques clairs et interactifs (radars, barres).
*   **Interface Multilingue** : Application disponible en plusieurs langues (grâce au système i18n).

---

## 📊 Méthodologie du Projet

Le système fonctionne en plusieurs étapes claires. Voici le pipeline complet :

```
📄 PDF / DOCX  →  📝 Texte (Markdown)  →  📋 JSON  →  📐 Vecteurs  →  🏆 Score
   (Étape 1)          (Étape 2)           (Étape 3)      (Étape 4)
```

### Étape 1 : PDF / DOCX → Texte Markdown (Parsing)
Le système reçoit un fichier (PDF ou DOCX). Il utilise des outils spécialisés (**Docling**, **PyMuPDF**, et **Pytesseract**) pour "lire" le document, comprendre la présentation (titres, tableaux) et le transformer en texte propre au format **Markdown**.

### Étape 2 : Texte Markdown → JSON (Extraction)
Le texte Markdown est ensuite envoyé à notre modèle d'Intelligence Artificielle (**Ollama**). L'IA lit le texte et en extrait les informations importantes pour créer un profil de candidat structuré au format **JSON** (validé par **Pydantic**). Elle trouve :
*   Les informations de contact (téléphone, email).
*   Les compétences techniques (Hard skills) et humaines (Soft skills).
*   Les années d'expérience et l'historique de travail.
*   L'éducation et les diplômes.

### Étape 3 : JSON → Vecteurs (Embeddings)
Le profil JSON structuré (de l'Étape 2) est transformé en nombres (vecteurs mathématiques) grâce aux modèles **Sentence-Transformers** et **FlagEmbedding**. Ces vecteurs sont stockés dans notre base de données cloud (**Neon PostgreSQL** avec l'extension **pgvector**). Le système fait la même chose avec l'offre d'emploi.

### Étape 4 : Vecteurs → Score (Scoring et Matching)
Enfin, le système utilise les vecteurs pour calculer le score final du candidat :
1.  **Comparaison mathématique** : Il utilise le modèle **bge-reranker-v2.5** pour comparer les vecteurs du CV et de l'offre d'emploi.
2.  **Vérification des critères** : Il vérifie (via **FastAPI** et **Python**) si les exigences strictes sont respectées (par exemple, le nombre d'années d'expérience).
3.  **Évaluation par l'IA** : Le modèle (**Ollama** avec `llama3` ou `Qwen`) agit comme un recruteur expert. Il donne une note finale (de 0 à 100), explique les **points forts**, les **points faibles**, et donne une **recommandation**.

---

## 🛡️ Technologies de Secours (Fallbacks)

Le système est robuste et conçu pour fonctionner même si un outil principal échoue :
*   **PyMuPDF (fitz)** : Utilisé si l'outil principal (*Docling*) n'arrive pas à lire un fichier PDF.
*   **Pytesseract (OCR) & Pillow** : Utilisés pour lire le texte sur des CV sous forme d'image (documents scannés), quand la lecture de texte normale échoue.
*   **Extraction par Regex (Expressions régulières)** : Utilisée pour trouver les emails, les téléphones et les compétences (avec des mots-clés) si le modèle d'IA principal (*Ollama*) ne répond pas.
*   **Extraction XML (zipfile & ElementTree)** : Utilisée pour lire le texte des fichiers DOCX de manière basique en cas de problème.

---

## 💻 Technologies et Bibliothèques Utilisées

Voici la liste complète des outils qui font fonctionner ce projet :

### Frontend (Interface Utilisateur)
*   **React 19** & **TypeScript** - Pour créer l'interface principale avec un code sûr.
*   **Vite** - Pour compiler et lancer le projet rapidement.
*   **Tailwind CSS** (avec **clsx** et **tailwind-merge**) - Pour un design moderne et qui s'adapte à tous les écrans.
*   **Recharts** - Pour créer de superbes graphiques visuels.
*   **Axios** - Pour communiquer avec le serveur.
*   **Lucide React** - Pour les icônes.
*   **Firebase** - Pour des services supplémentaires (authentification, etc.).

### Backend (Serveur et Base de Données)
*   **FastAPI** & **Uvicorn** - Pour créer une API très rapide en Python (3.11+).
*   **Neon (PostgreSQL)** & **psycopg2** - Une base de données cloud qui gère les vecteurs (`pgvector`). *Note: ChromaDB est aussi disponible pour des tests locaux.*
*   **SQLAlchemy & Alembic** - Pour gérer la base de données.
*   **Pydantic** - Pour vérifier que les données reçues sont correctes.
*   **Python-jose & Passlib** - Pour la sécurité (mots de passe et tokens).

### IA et Traitement du Langage (NLP)
*   **Ollama** - Pour faire fonctionner les modèles d'IA localement (comme `llama3` ou `Qwen3:8B`).
*   **Tenacity** - Pour gérer les erreurs et relancer l'IA en cas de problème.
*   **Docling 2.x, PyMuPDF & pymupdf4llm** - Pour lire les documents PDF et DOCX complexes.
*   **Pytesseract & Pillow** - Pour lire le texte sur les images (technologie OCR).
*   **Sentence-Transformers & FlagEmbedding** - Pour transformer le texte en vecteurs.
*   **BAAI/bge-m3 & bge-reranker-v2.5** - Modèles avancés pour comparer les textes avec précision.

---

## 🚀 Lancement du Projet en Local

**1. Base de données (Neon PostgreSQL)**
Créez un fichier `.env` dans le dossier `backend/` et ajoutez votre lien Neon :
```env
DATABASE_URL="postgresql://user:password@ep-xxxxx.neon.tech/neondb?sslmode=require"
```

**2. Démarrer le Backend (Serveur)**
Ouvrez votre terminal et tapez :
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Sur Windows : .\app\.venv\Scripts\Activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```
*Note : Le projet peut aussi être lancé avec Docker (`docker-compose up`) ou sur Kaggle (voir `KAGGLE_BACKEND.md`).*

**3. Démarrer le Frontend (Interface)**
Ouvrez un autre terminal et tapez :
```bash
cd frontend
npm install
npm run dev
```
Ouvrez ensuite `http://localhost:5173` dans votre navigateur.
