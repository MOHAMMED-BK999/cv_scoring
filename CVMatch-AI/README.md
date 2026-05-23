# CVMatch-AI — Architecture et Stack Technique 🚀

Ce dépôt contient le projet **CVMatch-AI**, un système avancé propulsé par l'IA conçu pour analyser, extraire et évaluer automatiquement les CV des candidats par rapport aux fiches de poste, en utilisant des modèles NLP de pointe (State-of-the-Art).

---

## ⚙️ Le Workflow du Moteur IA 

Le cœur de ce projet est un pipeline d'Intelligence Artificielle multi-étapes très avancé. Lorsqu'un recruteur télécharge un CV, celui-ci passe par le flux de travail automatisé suivant :

### Étape 1 : Parsing de Documents (Visuel vers Texte)
Le moteur reçoit un fichier PDF ou DOCX brut. Au lieu de lire aveuglément le texte ligne par ligne, il utilise **Docling 2.x** et **PyMuPDF** pour comprendre visuellement la mise en page (colonnes, tableaux, en-têtes) et convertit le document en un format **Markdown** proprement structuré.

### Étape 2 : Extraction d'Informations (Sortie Structurée)
Le Markdown brut est envoyé à notre LLM local (**Ollama**). Grâce à la bibliothèque **Instructor**, le LLM est contraint de générer un objet JSON strictement typé (validé via Pydantic). Il extrait et catégorise :
*   Les informations de contact
*   Les compétences techniques (Hard skills) et comportementales (Soft skills)
*   Les années d'expérience et l'historique détaillé des emplois
*   L'éducation et les diplômes

### Étape 3 : Embeddings Vectoriels
Le profil structuré du candidat est converti en vecteurs mathématiques denses à l'aide du modèle d'embedding **SentenceTransformer**. Ces vecteurs sont ensuite stockés dans notre base de données cloud (**Neon PostgreSQL**) à l'aide de l'extension `pgvector`. Le même processus est appliqué à la fiche de poste.

### Étape 4 : Scoring Multi-Niveaux et Matching
Le système ne se contente pas de deviner un score ; il le calcule de manière rigoureuse :
1.  **Récupération Sémantique (Retrieve)** : Il calcule la similarité cosinus entre les embeddings du CV et ceux de la fiche de poste pour trouver le chevauchement conceptuel.
2.  **Scoring Heuristique** : Il exécute des vérifications mathématiques pour s'assurer que les exigences strictes sont respectées (par exemple, *Le candidat a-t-il exactement 4 ans d'expérience ? Possède-t-il les compétences exactes requises ?*).
3.  **LLM-as-a-Judge (Évaluateur IA)** : Enfin, le profil et la fiche de poste sont renvoyés à **Ollama**. Agissant comme un auditeur RH expert, le LLM évalue le candidat de manière critique sur une échelle de 0 à 100 en se basant sur les Compétences, l'Expérience, l'Éducation et la Compatibilité. Il génère également une explication claire mettant en évidence les **Forces**, les **Lacunes (Gaps)** et une **Recommandation** finale.

---

## 💻 Stack Technique

Voici la liste complète des technologies propulsant cette application :

### Frontend
Une Single Page Application moderne et ultra-rapide conçue pour permettre aux recruteurs de télécharger facilement des CV, de consulter des tableaux de bord analytiques et de gérer les candidats.
*   **React 19** - Framework UI principal
*   **TypeScript** - Pour un typage strict et une expérience de développement robuste
*   **Vite** - Bundler haute performance et serveur de développement
*   **Tailwind CSS** - Framework CSS utilitaire pour un style réactif et esthétique
*   **Recharts** - Utilisé pour le rendu des graphiques interactifs en radar et la distribution des scores
*   **Axios** - Client HTTP pour la communication avec l'API backend

### Backend
Une API REST asynchrone et robuste pilotant les pipelines complexes de NLP.
*   **FastAPI (Python 3.11+)** - Framework backend haute performance
*   **Neon (PostgreSQL Serverless)** - Base de données cloud principale, utilisant spécifiquement l'extension **`pgvector`** pour stocker et interroger les embeddings vectoriels denses
*   **SQLAlchemy & Alembic** - ORM et gestion des migrations de base de données
*   **Pydantic** - Validation des données et application des schémas

### IA & Modèles NLP
*   **Ollama** - Moteur d'inférence LLM local exécutant des modèles tels que `llama3` ou `Qwen3:8B`
*   **Instructor** - Garantit des sorties JSON structurées et parfaitement typées du LLM
*   **Docling 2.x & PyMuPDF** - Parsing de documents visuels de pointe
*   **BAAI/bge-m3** - Embeddings de texte avancés supportant les vecteurs denses
*   **bge-reranker-v2.5** - Modèle de reranking (Cross-encoder) pour une correspondance CV/Job ultra-précise

---

## 🚀 Comment lancer le projet localement

**1. Base de données (Neon)**
Créez un fichier `.env` dans le répertoire `backend/` avec votre chaîne de connexion Neon :
```env
DATABASE_URL="postgresql://user:password@ep-xxxxx.neon.tech/neondb?sslmode=require"
```

**2. Backend (FastAPI)**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Ou .\app\.venv\Scripts\Activate sur Windows
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

**3. Frontend (React/Vite)**
```bash
cd frontend
npm install
npm run dev
```
