# FinPulse Quick Start Guide

Get FinPulse up and running in 5 minutes!

## Prerequisites Check

- [ ] Python 3.9+ installed (`python --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] Docker installed (for PostgreSQL) OR PostgreSQL 14+ installed locally

## Quick Setup

### 1. Start PostgreSQL (using Docker)

```bash
docker-compose up -d
```

This will start PostgreSQL on port 5432 with:
- Database: `finpulse`
- User: `finpulse`
- Password: `finpulse`

### 2. Backend Setup (Terminal 1)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example.txt .env
# Edit .env and change SECRET_KEY to a secure random string

# Start the server
python run.py
# OR
uvicorn app.main:app --reload
```

Backend will run on `http://localhost:8000`
API docs available at `http://localhost:8000/docs`

### 3. Frontend Setup (Terminal 2)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on `http://localhost:5173`

### 4. First Steps

1. Open `http://localhost:5173` in your browser
2. Click "Register" to create an account
3. Login with your credentials
4. You'll see the dashboard (will be empty initially)

### 5. Add Some Data

**Option A: Using the API (via `/docs`)**

1. Go to `http://localhost:8000/docs`
2. Authorize with your JWT token (get it from login endpoint)
3. Create an account: `POST /api/accounts/`
   ```json
   {
     "type": "checking",
     "institution_name": "My Bank",
     "balance": 10000.0
   }
   ```
4. Create transactions: `POST /api/transactions/`
   ```json
   {
     "account_id": 1,
     "amount": -50.0,
     "category": "food",
     "description": "Grocery shopping"
   }
   ```

**Option B: Using CSV Upload**

1. Create a CSV file with your transactions:
   ```csv
   amount,category,description,timestamp
   -50.00,food,Grocery Store,2024-01-15T10:00:00
   5000.00,salary,Monthly Salary,2024-01-01T09:00:00
   -1200.00,rent,Monthly Rent,2024-01-05T08:00:00
   ```
2. Upload via API: `POST /api/transactions/upload` (include the CSV file and account_id)

## Troubleshooting

**Backend won't start:**
- Check PostgreSQL is running: `docker ps`
- Verify DATABASE_URL in `.env` matches your PostgreSQL setup
- Check port 8000 is not already in use

**Frontend can't connect to backend:**
- Verify backend is running on port 8000
- Check `VITE_API_URL` in frontend `.env` (or use default)
- Check browser console for CORS errors

**Database connection errors:**
- Verify PostgreSQL container is running: `docker-compose ps`
- Check database credentials in `backend/.env`
- Try recreating the database: `docker-compose down -v && docker-compose up -d`

**Import errors:**
- Make sure you activated the virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (need 3.9+)

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the API documentation at `http://localhost:8000/docs`
- Check out the design document in [DESIGNDOC.md](DESIGNDOC.md)

## Support

If you encounter issues, check:
1. All prerequisites are installed correctly
2. Environment variables are set properly
3. Ports 8000 (backend) and 5173 (frontend) are available
4. Database is running and accessible

