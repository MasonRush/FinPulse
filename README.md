# FinPulse - Financial Health Dashboard

A comprehensive financial health platform that aggregates assets, liabilities, and monthly cash flow to provide a "Financial Health Score" and investment performance tracking.

## Features

- **Financial Dashboard**: Real-time overview of net worth, income, expenses, and savings rate
- **Investment Tracking**: Monitor portfolio performance with ROI calculations and asset allocation
- **Transaction Management**: Upload CSV files from banks and track expenses by category
- **Visual Analytics**: Interactive charts for net worth trends and expense distribution
- **Secure Authentication**: JWT-based authentication with Argon2 password hashing

## Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **PostgreSQL**: Relational database for complex financial data
- **SQLAlchemy**: ORM for database operations
- **Pandas**: Data processing for CSV uploads and aggregations
- **JWT + Argon2**: Secure authentication and password hashing

### Frontend
- **React + Vite**: Modern, fast frontend framework
- **TypeScript**: Type-safe development
- **Shadcn UI**: Beautiful, accessible UI components
- **Recharts**: Interactive data visualization
- **Tailwind CSS**: Utility-first CSS framework

## Project Structure

```
FinPulse/
├── backend/
│   ├── app/
│   │   ├── routers/      # API route handlers
│   │   ├── models.py     # Database models
│   │   ├── schemas.py    # Pydantic schemas
│   │   ├── security.py   # Authentication & authorization
│   │   ├── database.py   # Database configuration
│   │   └── main.py       # FastAPI application
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── lib/          # Utilities & API client
│   │   └── App.tsx
│   └── package.json
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- Docker (optional, for PostgreSQL)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Copy `env.example.txt` to `.env` in the `backend` directory and update the values:
   ```bash
   cp env.example.txt .env
   # Edit .env with your configuration
   ```

5. **Set up PostgreSQL database**:
   Option A: Using Docker Compose (recommended):
   ```bash
   docker-compose up -d
   ```
   
   Option B: Manual PostgreSQL setup:
   ```sql
   CREATE DATABASE finpulse;
   CREATE USER finpulse WITH PASSWORD 'finpulse';
   GRANT ALL PRIVILEGES ON DATABASE finpulse TO finpulse;
   ```

6. **Run database migrations** (tables are auto-created on first run):
   The application will automatically create tables on startup.

7. **Start the backend server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`
   API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Create environment file** (optional):
   Copy `env.example.txt` to `.env` in the `frontend` directory:
   ```bash
   cp env.example.txt .env
   # Edit .env if needed (defaults work for local development)
   ```

4. **Start the development server**:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

## Usage

1. **Register a new account** at `http://localhost:5173/register`
2. **Login** with your credentials
3. **Create accounts** (checking, savings, brokerage, loan) via the API or frontend
4. **Upload transactions** via CSV file or create them manually
5. **View your dashboard** with financial metrics and charts

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token

### Dashboard
- `GET /api/dashboard/summary` - Get financial summary (net worth, income, expenses, savings rate)

### Accounts
- `GET /api/accounts/` - List all accounts
- `POST /api/accounts/` - Create a new account
- `GET /api/accounts/{id}` - Get account details

### Transactions
- `GET /api/transactions/` - List transactions
- `POST /api/transactions/` - Create a transaction
- `POST /api/transactions/upload` - Upload CSV file with transactions

### Investments
- `GET /api/investments/` - List portfolio holdings
- `POST /api/investments/` - Add portfolio holding
- `GET /api/investments/performance` - Get investment performance metrics

## CSV Upload Format

When uploading transactions via CSV, include the following columns:

```csv
amount,category,description,timestamp
-50.00,food,Grocery Store,2024-01-15T10:00:00
5000.00,salary,Monthly Salary,2024-01-01T09:00:00
-1200.00,rent,Monthly Rent,2024-01-05T08:00:00
```

**Categories**: food, rent, salary, utilities, transportation, entertainment, shopping, healthcare, education, other

## Development

### Running Tests

```bash
# Backend tests (when implemented)
cd backend
pytest

# Frontend tests (when implemented)
cd frontend
npm test
```

### Building for Production

```bash
# Frontend
cd frontend
npm run build

# Backend
# Use a production ASGI server like gunicorn with uvicorn workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

