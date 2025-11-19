# Setup Guide

## Quick Start with Docker (Recommended)

1. **Start all services:**
   ```bash
   docker-compose up -d
   ```

2. **Seed sample data:**
   ```bash
   docker-compose exec backend python seed_data.py
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Manual Setup

### Backend Setup

1. **Navigate to backend:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL:**
   - Install PostgreSQL
   - Create database: `createdb dataset_platform`
   - Update DATABASE_URL in `.env` file

5. **Create .env file:**
   ```bash
   DATABASE_URL=postgresql://user:password@localhost:5432/dataset_platform
   ```

6. **Run migrations (tables auto-create on first run):**
   ```bash
   python -m app.main
   ```

7. **Seed sample data:**
   ```bash
   python seed_data.py
   ```

8. **Start server:**
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. **Navigate to frontend:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create .env file (optional):**
   ```bash
   VITE_API_URL=http://localhost:8000
   ```

4. **Start development server:**
   ```bash
   npm run dev
   ```

## Testing the Platform

1. **Access the frontend** at http://localhost:3000
2. **Browse datasets** using the search functionality
3. **View recommendations** on the home page
4. **Purchase a dataset** (uses demo user with ID 1 and balance of $1000)

## Sample Credentials

After running `seed_data.py`, you can use:
- **Buyer**: email: `buyer@example.com`, password: `password123`
- **Seller**: email: `seller@example.com`, password: `password123`

Note: Authentication endpoints are not fully implemented in this version. User IDs are hardcoded for demo purposes.

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env file
- Verify database exists

### Port Conflicts
- Backend default: 8000
- Frontend default: 3000
- PostgreSQL default: 5432
- Change ports in docker-compose.yml if needed

### Docker Issues
- Ensure Docker and Docker Compose are installed
- Check logs: `docker-compose logs`
- Restart services: `docker-compose restart`

