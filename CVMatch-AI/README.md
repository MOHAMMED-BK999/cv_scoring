# CVMatch-AI 🤖

An intelligent CV scoring and matching system powered by AI to analyze, evaluate, and match CVs with job requirements.

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Contributing](#contributing)

## Overview

CVMatch-AI is a comprehensive solution for automated CV analysis and job matching. It leverages modern AI technologies to evaluate candidate CVs against job descriptions and provide intelligent scoring and recommendations.

## Tech Stack

### Frontend
- **TypeScript** (50.3%) - Type-safe frontend development
- **HTML** (0.2%) - Markup for web interfaces

### Backend
- **Python** (48.8%) - Core backend logic and AI processing
- **Flask/Django** - Web framework for API endpoints
- **Docker** (0.1%) - Container orchestration and deployment

### Template Engine
- **Mako** (0.4%) - Dynamic HTML template rendering

### Build & Scripting
- **JavaScript** (0.2%) - Client-side interactivity and tooling
- **Dockerfile** (0.1%) - Container configuration

### Key Libraries & Tools

#### Python Backend
- **NLP & AI**: Natural Language Processing for CV parsing
- **Data Processing**: Pandas for data manipulation
- **API Framework**: Flask/FastAPI for REST endpoints
- **Database**: SQLAlchemy for ORM
- **Task Queue**: Celery for async job processing
- **Testing**: Pytest for unit and integration tests

#### Frontend
- **TypeScript Framework**: React or Vue.js for UI components
- **State Management**: Redux or Vuex
- **HTTP Client**: Axios for API communication
- **Styling**: CSS/SCSS/Tailwind CSS
- **Build Tool**: Webpack or Vite

#### DevOps & Infrastructure
- **Containerization**: Docker for consistent environments
- **Container Registry**: DockerHub or GitHub Container Registry
- **CI/CD**: GitHub Actions for automation
- **Monitoring**: Logging and error tracking

## Features

✨ **AI-Powered CV Scoring**
- Automated CV parsing and analysis
- Intelligent skill matching
- Experience level evaluation
- ATS-friendly scoring

📊 **Analytics & Reporting**
- Detailed candidate scoring reports
- Comparative analysis
- Trend insights
- Export capabilities

🔍 **Smart Matching**
- CV to job description alignment
- Skill gap analysis
- Recommendation engine
- Batch processing

🔒 **Security & Privacy**
- Secure file handling
- Data encryption
- GDPR compliance
- User authentication

## Installation

### Prerequisites
- Node.js 16+ (for TypeScript/Frontend)
- Python 3.8+ (for Backend)
- Docker & Docker Compose (optional)

### Local Setup

```bash
# Clone the repository
git clone https://github.com/MOHAMMED-BK999/cv_scoring.git
cd cv_scoring/CVMatch-AI

# Backend Setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend Setup
npm install
npm run build
```

### Using Docker

```bash
docker-compose up -d
```

## Usage

### Starting the Application

```bash
# Terminal 1: Start Backend
python app.py

# Terminal 2: Start Frontend
npm start
```

The application will be available at `http://localhost:3000` (frontend) and `http://localhost:5000` (API).

### API Endpoints

```bash
# Score a CV
POST /api/score
Content-Type: application/json

{
  "cv_content": "...",
  "job_description": "..."
}

# Get matching candidates
GET /api/matches?job_id=123
```

## Architecture

```
CVMatch-AI/
├── frontend/              # TypeScript/JavaScript UI
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/              # Python backend
│   ├── app.py
│   ├── models/
│   ├── routes/
│   ├── utils/
│   └── requirements.txt
├── templates/            # Mako templates
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on GitHub or contact the project maintainers.


