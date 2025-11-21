# Dataset Selling Platform

A scalable, multi-agent system platform for buying and selling datasets. This platform allows end users to search, browse, and purchase datasets with an intelligent agent-based architecture.

## Features

- **Multi-Agent System**: Four specialized agents working together:
  - **Search Agent**: Intelligent dataset search with filtering and sorting
  - **Recommendation Agent**: Personalized dataset recommendations based on user behavior
  - **Transaction Agent**: Handles purchases and payment processing
  - **Support Agent**: Provides user support and answers queries

- **Scalable Architecture**:
  - FastAPI backend with async support
  - React frontend with modern UI
  - PostgreSQL database
  - Docker containerization for easy deployment
  - Microservices-ready structure

- **Core Functionality**:
  - Dataset browsing and search
  - Advanced filtering (category, price, rating, tags)
  - Dataset recommendations
  - Purchase management
  - User management

## Tooling & Software Requirements

Install these tools before working on the project:

- **Git** 2.40+ for version control (`git --version`)
- **Docker Desktop** with **Docker Compose** v2 for container orchestration (`docker --version`, `docker compose version`)
- **Python** 3.11+ with `pip` for backend development (`python3 --version`)
- **Node.js** 18+ with `npm` for the frontend (`node --version`)
- **PostgreSQL** 14+ (server + `psql`) if you want to run the database outside Docker
- *(Optional)* **pgAdmin** or another SQL client for inspecting tables and data

> Tip: On macOS you can install most dependencies via Homebrew: `brew install git python node postgresql`.

## Architecture

### Backend Structure
```
backend/
├── app/
│   ├── agents/          # Multi-agent system
│   │   ├── base_agent.py
│   │   ├── search_agent.py
│   │   ├── recommendation_agent.py
│   │   ├── transaction_agent.py
│   │   ├── support_agent.py
│   │   └── agent_orchestrator.py
│   ├── api/             # API endpoints
│   ├── models/           # Database models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   └── main.py          # FastAPI application
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/      # Reusable components
│   ├── pages/          # Page components
│   ├── services/       # API services
│   └── App.jsx         # Main app component
```

## Database Setup

You can rely on the PostgreSQL service defined in `docker-compose.yml` or provision your own local instance. For a manual/local Postgres setup:

1. Start PostgreSQL (ensure it listens on `localhost:5432`).
2. Create the database and user:
   ```bash
   createdb dataset_platform
   createuser dataset_user --pwprompt
   psql -d dataset_platform -c "GRANT ALL PRIVILEGES ON DATABASE dataset_platform TO dataset_user;"
   ```
3. Copy `backend/.env.example` to `backend/.env` and update:
   ```
   DATABASE_URL=postgresql+asyncpg://dataset_user:<password>@localhost:5432/dataset_platform
   ```
4. The first backend run will auto-create tables via SQLModel.

Prefer Docker? From the repo root run:
```bash
docker compose up db -d
```
The service uses credentials from `.env` / `.env.example`.

## First-Time Local Run

1. **Clone & prepare directories**
   ```bash
   git clone <repository-url>
   cd Agent-sample
   ```
2. **Configure environment variables**
   - Copy `.env.example` to `.env` at the repo root (for Docker Compose) and within `backend/`.
   - Update secrets: `POSTGRES_PASSWORD`, `DATABASE_URL`, `JWT_SECRET`, etc.
3. **Install backend dependencies**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. **Install frontend dependencies**
   ```bash
   cd ../frontend
   npm install
   ```
5. **Start services**
   - *Docker path*: from repo root run `docker compose up -d` to boot Postgres, backend, and frontend together.
   - *Manual path*: ensure Postgres is running, then start the backend with `uvicorn app.main:app --reload` and the frontend with `npm run dev`.
6. **Verify**
   - Frontend at `http://localhost:3000`
   - API docs at `http://localhost:8000/docs`
   - Database tables visible via `psql`/pgAdmin

## Quick Run Reference
These are the exact commands to run the application locally:

### 1. Database (Docker)
From project root:
```bash
docker compose up db -d
```

### 2. Backend
From `backend/` directory:
```bash
# Activate venv if not already active
source venv/bin/activate
# Run server
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend
From `frontend/` directory:
```bash
npm run dev
```

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)

### Quick Start with Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd Agent-sample
```

2. Start all services:
```bash
docker-compose up -d
```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Backend

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp ../.env.example .env
# Edit .env with your configuration
```

5. Run database migrations (create tables):
```bash
# The tables are auto-created on first run
python -m app.main
```

6. Start the server:
```bash
uvicorn app.main:app --reload
```

#### Frontend

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

## API Endpoints

### Datasets
- `GET /api/datasets/` - List all datasets
- `GET /api/datasets/search` - Search datasets (with filters)
- `GET /api/datasets/{id}` - Get dataset details
- `GET /api/datasets/recommendations/{user_id}` - Get recommendations
- `POST /api/datasets/` - Create dataset (seller)
- `PUT /api/datasets/{id}` - Update dataset

### Purchases
- `POST /api/purchases/` - Purchase a dataset
- `GET /api/purchases/user/{user_id}` - Get user purchases
- `GET /api/purchases/{id}` - Get purchase details

### Support
- `POST /api/support/query` - Submit support query

### Users
- `POST /api/users/` - Create user
- `GET /api/users/{id}` - Get user details

## Multi-Agent System

The platform uses a multi-agent architecture where specialized agents handle different tasks:

1. **SearchAgent**: Processes search queries with advanced filtering
2. **RecommendationAgent**: Uses collaborative filtering and popularity metrics
3. **TransactionAgent**: Handles purchase transactions and balance management
4. **SupportAgent**: Provides FAQ and support responses

Agents are orchestrated through the `AgentOrchestrator` which can execute single tasks or complex workflows.

## Database Schema

- **Users**: User accounts (buyers and sellers)
- **Datasets**: Dataset listings with metadata
- **Purchases**: Transaction records

## Future Scalability Considerations

1. **Horizontal Scaling**: 
   - Backend can be scaled with load balancers
   - Database can use read replicas
   - Frontend can be served via CDN

2. **Caching Layer**:
   - Redis for session management
   - Cache popular searches and recommendations

3. **Message Queue**:
   - RabbitMQ/Kafka for async processing
   - Background jobs for dataset processing

4. **Search Enhancement**:
   - Elasticsearch for advanced full-text search
   - Vector search for semantic similarity

5. **Microservices**:
   - Split agents into separate services
   - API Gateway for routing
   - Service mesh for inter-service communication

6. **Monitoring & Observability**:
   - Prometheus for metrics
   - Grafana for visualization
   - Distributed tracing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License

## Support

For support queries, use the support API endpoint or create an issue in the repository.

