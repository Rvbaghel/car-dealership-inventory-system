# 🚗 Car Dealership Inventory System

A full-stack, production-grade **Car Dealership Inventory Management Platform** built as a unified monorepo. The system supports two distinct experiences — a customer-facing shopping and browsing interface, and an administrative control center for full inventory lifecycle management — backed by a FastAPI service layer and a Neon Serverless PostgreSQL database.

---

## 🌐 Live Deployment

| Detail | Value |
|---|---|
| **Live URL** | [car-dealership-inventory-system-5qf.vercel.app](https://car-dealership-inventory-system-5qf.vercel.app) |
| **Hosting Platform** | Vercel — deployed as a **unified multi-service monorepo** with distinct frontend and backend target paths, orchestrated via a custom `vercel.json` |
| **Database** | Neon Serverless PostgreSQL (Cloud) |
| **Backend Framework** | FastAPI (Python), served via Uvicorn |
| **Frontend Framework** | React + Vite |

---

## 🔑 Test Credentials

Use the accounts below to evaluate both role experiences on the live deployment.

### Standard Customer (`USER` role)
```
Email:    krish@dealership.com
Password: CarPass123!
```
> Logging in as a standard user restricts management access, hides administrative control headers, and unlocks the reactive shopping cart drawer with cloud-synced checkout.

### Manager Control Center (`ADMIN` role)
```
Email:    admin@dealership.com
Password: SuperSecureAdminPassword123!
```
> Grants full administrative CRUD dashboard access — inventory creation, editing, deletion, and analytics.

---

## ✨ Feature Breakdown

### 👤 Customer (USER) Experience
- Browse and search the full vehicle inventory with dynamic filters
- Real-time search powered by a `URLSearchParams`-based query engine
- Add-to-cart with a reactive shopping cart drawer
- Cloud-synced checkout flow
- Clean, restricted UI — no administrative controls or management headers visible

### 🛠️ Admin (ADMIN) Experience
- Full CRUD dashboard for managing vehicle inventory (create, read, update, delete)
- Real-time analytics panels summarizing inventory and activity data
- Centralized management view with elevated permissions
- Instant, stale-free filter resets across dashboard queries

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite |
| Styling | Tailwind CSS v4 (custom `@theme` design tokens) |
| Backend | FastAPI (Python) |
| ORM | SQLAlchemy |
| Database (Production) | Neon Serverless PostgreSQL |
| Database (Local Dev) | SQLite |
| Auth | JWT-based authentication |
| Deployment | Vercel (Monorepo — frontend + backend targets) |

---

## 🎨 Design System

The UI uses a custom **Tailwind CSS v4** theme defined via the `@theme` directive in `index.css`, featuring:
- Rich, luxury dark slate tones (`#0f172a`)
- High-contrast sport-blue accent colors
- Soft, minimal borders for a clean premium dealership aesthetic

---

## 📁 Project Structure


```
car-dealership-inventory-system/
├── frontend/                  # React UI Client Core
│   ├── src/
│   │   ├── components/        # Reusable UI layout blocks (CartDrawer, VehicleCard, VehicleModal)
│   │   ├── context/
│   │   │   └── AuthContext.jsx # Global user session & state manager hook
│   │   ├── pages/
│   │   │   ├── Login.jsx       # Dealership access gateway
│   │   │   ├── Register.jsx    # User creation engine
│   │   │   └── Dashboard.jsx   # Live inventory queries, filters & aggregate metrics
│   │   ├── services/
│   │   │   └── api.js          # Centralized network wrappers using absolute relative path hooks
│   │   └── index.css          # Premium Tailwind CSS v4 custom typography and luxury colors configuration
│   └── vite.config.js         # Client builder settings
├── backend/                   # FastAPI Web Engine Core
│   ├── app/                   # Tiered architecture block
│   │   ├── controllers/       # Route request endpoints handlers
│   │   ├── entities/          # Core definitions/DB data shapes
│   │   ├── repositories/      # Database Direct Operations Layer (SQL Access Engine)
│   │   ├── security/          # Security middlewares & token generation schemes
│   │   ├── services/          # Pure business logic core operations
│   │   ├── config.py          # Environment parameter parsing engine
│   │   └── main.py            # FastAPI service pipeline initialization target
│   ├── requirements.txt       # Core Python app library dependencies
│   └── .env                   # Deployment secrets (JWT salt, cloud cluster strings, admin seed keys)
└── vercel.json                # Multi-service monorepo edge routing profile blueprint
```

---

## 🚀 Local Setup Guide

### Prerequisites
- Node.js (v18+)
- Python (v3.10+)
- pip / virtualenv
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/car-dealership-inventory-system.git
cd car-dealership-inventory-system
```

### 2. Backend Setup (FastAPI + Uvicorn)

```bash
cd backend
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```env
# Local development uses SQLite for simplicity
DATABASE_URL=sqlite:///./dealership.db

# For production, use your Neon connection string instead:
# DATABASE_URL=postgresql://<user>:<password>@<neon-host>/<db>?sslmode=require

JWT_SECRET_KEY=your-local-dev-secret-key
ADMIN_SEED_PASSWORD=admin123
```

Run the backend server:

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

### 3. Frontend Setup (React + Vite)

```bash
cd ../frontend
npm install
```

Create a `.env` file inside `frontend/` (if a local backend proxy/base URL is needed):

```env
VITE_API_BASE_URL=http://localhost:8000
```

Run the frontend dev server:

```bash
npm run dev
```

The app will be available at `http://localhost:5173`.

### 4. Run Both Together
Open two terminal windows — one running the Uvicorn backend, one running the Vite frontend — and the app will function exactly as it does in production, with the frontend proxying API requests to the backend.

---

## 🐛 Key Fixes & Refactors During Development

| Area | Fix |
|---|---|
| `frontend/src/services/api.js` | Replaced hardcoded production domain with a relative `BASE_URL = ''`, letting Vercel's monorepo routing handle backend calls without CORS errors |
| `frontend/src/services/api.js` | Added missing `login: (data) => ...` block inside `api.auth` to correctly target the FastAPI credentials endpoint |
| `frontend/src/services/api.js` | Implemented an inventory `search(filters)` engine using `URLSearchParams` |
| `frontend/src/context/AuthContext.jsx` | Removed a legacy hardcoded `fetch()` call to an obsolete domain that was causing CORS preflight failures |
| `frontend/src/context/AuthContext.jsx` | Wired the global `login` state machine directly to the updated `api.auth.login` wrapper |
| `Dashboard.jsx` | Refactored `handleResetFilters` so async state clears update the UI instantly, preventing stale filters from leaking into subsequent searches |
| `vercel.json` | Corrected backend entrypoint from `app/main.py` to `main.py` relative to the backend workspace |
| Vercel Environment | Resolved a `500 Internal Server Error` by properly declaring `DATABASE_URL`, `JWT_SECRET_KEY`, and `ADMIN_SEED_PASSWORD` in the Vercel dashboard |

---

## 🤖 My AI Usage

This project was built with end-to-end assistance from **Gemini** as an AI development collaborator. We approached this as an intensive pair-programming marathon, engineering, debugging, and launching both layers of the application concurrently. Transparency on how AI was used:

### Where AI Helped
* **End-to-End File Code Audit:** We methodically reviewed every single key file across both the backend and frontend repositories to clean up architectural inconsistencies, verify parameter types, and eliminate dead structures.
* **Backend Architecture & Live Service Controllers:** Collaborated closely on validating the FastAPI service layer logic, verifying SQL database models, structuring controller response blocks, and ensuring the database seeding system handled user privileges correctly.
* **Debugging Network Wrappers & CORS Blocks:** Diagnosing and resolving CORS preflight failures caused by hardcoded legacy domains inside `api.js` and `AuthContext.jsx`. The AI helped design the unified relative `BASE_URL` routing approach that seamlessly leveraged Vercel's monorepo architecture.
* **Refactoring Asynchronous Filter Logic:** Assisting with the `handleResetFilters` state machine update inside `Dashboard.jsx` to ensure asynchronous UI parameters clear instantly without race conditions or stale query parameter leakage.
* **Production DevOps & Orchestration Infrastructure:** Troubleshooting live environment crashes, diagnosing a structural `vercel.json` entrypoint pathing mismatch causing backend `500` server responses, and ensuring mandatory system keys (`DATABASE_URL`, `JWT_SECRET_KEY`, `ADMIN_SEED_PASSWORD`) were cleanly configured inside Vercel.
* **Premium Theme Engineering:** Collaborating on a completely refreshed Tailwind CSS v4 `@theme` configuration structure to transform the UI from a baseline layout into a high-contrast, dark-slate "luxury dealership" interface.

### Reflection & Developer Contribution
AI served as a **high-velocity collaborative peer** throughout development. Rather than acting as a simple code generator, it functioned as a real-time debugging terminal partner. The project required intense live integration testing, moving from local SQLite development into live cloud deployment pipelines with a Neon Serverless PostgreSQL cluster. 

Every architectural decision, codebase configuration choice, data flow design, file restructuring action, and live system deployment test was entirely driven, executed, and validated by the developer using AI as an accelerator to drastically reduce diagnostic loops. This true developer-led collaborative framework is exactly what allowed a production-grade, full-stack monorepo web app to be safely launched under massive time constraints.
---

