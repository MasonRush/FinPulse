# Design Document: FinPulse Dashboard

## Project Goal

A comprehensive financial health platform that aggregates assets, liabilities, and monthly cash flow to provide a "Financial Health Score" and investment performance tracking.

## 1. System Overview

FinPulse is a full-stack application that moves beyond simple expense tracking. It acts as a financial command center where users can visualize their Net Worth growth, analyze spending categories, and track the ROI (Return on Investment) of their portfolios against market benchmarks (e.g., S&P 500).

## 2. Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Frontend | React (Vite) | Provides a responsive, single-page application experience. |
| UI/Charts | Shadcn UI + Recharts | Professional-grade tables/forms and high-performance SVG charts. |
| Backend | Python (FastAPI) | High-speed data processing and automatic documentation. |
| Calculations | Pandas | Used on the backend to aggregate millions of data points (transactions) in milliseconds. |
| Database | PostgreSQL | Relational database required to manage complex foreign-key relationships (User -> Account -> Transaction). |
| Security | JWT + Argon2 | Standard industry practices for secure session management and password hashing. |

## 3. Data Model (Schema)

To demonstrate systems thinking, the database is designed with high normalization:

- **Users**: ID, Username, Hashed Password, Currency Preference.
- **Accounts**: ID, UserID, Type (Checking, Savings, Brokerage, Loan), Institution Name.
- **Transactions**: ID, AccountID, Amount, Category (Food, Rent, Salary), Timestamp.
- **Portfolios**: ID, UserID, Ticker Symbols, Shares Owned, Cost Basis.

## 4. Key Features & Logic

### A. The "Investment Health" Audit

The backend doesn't just store data; it performs a Portfolio Audit.

- **Logic**: The FastAPI server fetches current market prices (via a free API like AlphaVantage or Yahoo Finance) and calculates the current value vs. the user's cost basis.
- **KPIs**: It calculates the Sharpe Ratio (risk-adjusted return) and Asset Allocation (e.g., "You are 80% in Tech, consider diversifying").

### B. Automated Budgeting

- **Logic**: Uses a simple classification algorithm (or keyword matching) to categorize expenses.
- **Metric**: Calculates the "Savings Rate" ($1 - \frac{Expenses}{Income}$) and projects a "Years to Retirement" based on current trends.

## 5. API Design (FastAPI)

### GET /dashboard/summary

- **Description**: Aggregates all accounts to return Net Worth, monthly cash flow, and top spending categories.
- **Calculation**: Sum(Assets) - Sum(Liabilities).

### POST /transactions/upload

- **Description**: Accepts CSV files from banks.
- **Logic**: The backend parses the CSV using Pandas, cleans the data, and bulk-inserts it into PostgreSQL.

### GET /investments/performance

- **Description**: Calculates Time-Weighted Return (TWR) for the user's stock portfolio.

## 6. UI/UX Design (Shadcn UI)

- **Executive Summary (Top)**: Four Card components showing Net Worth, Monthly Income, Monthly Expenses, and Investment Return %.
- **Interactive Charts (Center)**: 
  - A LineChart (Recharts) showing Net Worth over time.
  - A PieChart (Shadcn/Recharts) showing expense distribution.
- **Transaction Ledger (Bottom)**: Uses the Shadcn DataTable component with built-in filtering, sorting, and pagination for high-volume data.
