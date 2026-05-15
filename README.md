# ✈️ Flight Bot - WhatsApp Flight Price Alerts

A production-ready Python bot that continuously monitors flight prices across major Brazilian and international airlines, delivering instant WhatsApp alerts when prices drop below your thresholds.

## 🎯 Features

- **24/7 Price Monitoring** — Automatically scans flights across 750+ airlines every 2 hours
- **Smart Deal Detection** — Identifies flights below configurable price thresholds
- **Dual User Tiers**:
  - 🆓 **Free Users** — Receive random flight deals in a public WhatsApp group every 6 hours
  - ⭐ **Paid Users** — Create personalized alerts with custom routes, dates, and price limits, receive instant direct messages
- **Multi-Airline Coverage** — Monitors all major Brazilian and international airlines
- **Advanced Filtering** — Filter by origin, destination, date range, and maximum price
- **Anti-Spam Protection** — Prevents duplicate alerts with configurable cooldown periods
- **Admin Dashboard** — Streamlit interface for managing routes, users, and monitoring alerts
- **RESTful API** — Complete CRUD endpoints for programmatic control
- **WhatsApp Commands** — Paid users can manage alerts directly via WhatsApp text commands
- **Production-Ready** — Docker, async/await, proper error handling, comprehensive logging

---

## 📋 Prerequisites

- **Docker & Docker Compose** (recommended) or
- **Python 3.11+**
- **Redis** (for caching)
- **WhatsApp Evolution API** instance (free or self-hosted)
- **Kiwi.com Tequila API key** (free, get at https://tequila.kiwi.com)

---

## 🚀 Quick Start

### 1. Clone or Download the Project

```bash
cd flight-bot
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```env
# Required
KIWI_API_KEY=your_kiwi_api_key_here
EVOLUTION_API_URL=http://localhost:8080  # or your self-hosted Evolution instance
EVOLUTION_API_KEY=your_evolution_api_key_here
FREE_GROUP_JID=120363xxx@g.us  # Get this from Evolution API

# Optional (defaults provided)
DATABASE_URL=sqlite+aiosqlite:///./flight_bot.db
REDIS_URL=redis://localhost:6379/0
```

### 3. Start with Docker Compose

```bash
docker-compose up --build
```

Services will be available at:
- **FastAPI Bot** → http://localhost:8000
- **Streamlit Admin** → http://localhost:8501
- **Redis** → localhost:6379

### 4. Access the Admin Dashboard

Open your browser to [http://localhost:8501](http://localhost:8501)

---

## 🔧 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `KIWI_API_KEY` | ✅ | - | Kiwi.com Tequila API key |
| `EVOLUTION_API_URL` | ✅ | - | Evolution API server URL |
| `EVOLUTION_API_KEY` | ✅ | - | Evolution API authentication key |
| `FREE_GROUP_JID` | ✅ | - | WhatsApp group JID for free users |
| `DATABASE_URL` | ❌ | sqlite+aiosqlite | Database connection string |
| `REDIS_URL` | ❌ | redis://localhost:6379/0 | Redis connection string |
| `SCAN_INTERVAL_MINUTES` | ❌ | 120 | How often to scan routes (in minutes) |
| `FREE_DIGEST_INTERVAL_HOURS` | ❌ | 6 | Frequency of free group digest (in hours) |
| `DEFAULT_DEAL_THRESHOLD_DOMESTIC_BRL` | ❌ | 299.0 | Default threshold for domestic routes |
| `DEFAULT_DEAL_THRESHOLD_INTL_BRL` | ❌ | 1499.0 | Default threshold for international routes |
| `ALERT_COOLDOWN_HOURS` | ❌ | 24 | Minimum hours between duplicate alerts |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Flight Bot Architecture                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────┐          ┌──────────────────┐    │
│  │  APScheduler    │          │  WhatsApp        │    │
│  │  (2h scan,      │          │  (Evolution API) │    │
│  │   6h digest)    │          │                  │    │
│  └────────┬────────┘          └──────────────────┘    │
│           │                            ▲               │
│           ▼                            │               │
│  ┌──────────────────┐          ┌──────────────────┐   │
│  │  Kiwi.com API    │          │  FastAPI Server  │   │
│  │  (Flight Search) │          │  (Port 8000)     │   │
│  └──────────────────┘          └──────────────────┘   │
│                                       ▲ ▼               │
│                                 ┌────────────┐          │
│                                 │ SQLAlchemy │          │
│                                 │  + Async   │          │
│                                 └─────┬──────┘          │
│                                       │                 │
│     ┌─────────────────────────────────┴─────────┐      │
│     ▼                    ▼                       ▼      │
│  ┌──────────┐    ┌──────────┐          ┌──────────┐   │
│  │ SQLite   │    │  Redis   │          │Streamlit │   │
│  │(Dev)     │    │(Cache)   │          │Dashboard │   │
│  └──────────┘    └──────────┘          │(Admin)   │   │
│                                         └──────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 📱 WhatsApp Commands for Paid Users

Once you upgrade to a paid account, send these commands via WhatsApp:

### Create Alert
```
/alerta GRU MIA 2026-08-01 2026-08-15 1500
```
Creates alert for GRU→MIA flights from Aug 1-15 with max price R$1500

### Create Alert to Any Destination
```
/alerta GRU qualquer 2026-07-01 2026-07-31 800
```
Alerts for any flight from GRU up to R$800 in July

### List Active Alerts
```
/listar
```

### Pause Alert
```
/pausar 3
```
Pauses alert #3 (doesn't delete it)

### Delete Alert
```
/deletar 3
```
Permanently removes alert #3

### View Account Status
```
/status
```

### Get Help
```
/ajuda
```

---

## 🔌 API Endpoints

All endpoints require the FastAPI server to be running on `http://localhost:8000`

### Routes Management

```bash
# List routes
GET /api/routes?skip=0&limit=100&active_only=true

# Get single route
GET /api/routes/{route_id}

# Create route
POST /api/routes
{
  "origin_iata": "GRU",
  "destination_iata": "MIA",
  "threshold_price": 1500.0
}

# Update route
PUT /api/routes/{route_id}
{
  "threshold_price": 1800.0,
  "is_active": true
}

# Delete route
DELETE /api/routes/{route_id}
```

### Users Management

```bash
# List users
GET /api/users?skip=0&limit=100&plan=paid&active_only=false

# Create user
POST /api/users
{
  "phone_number": "55XXXXXXXXXXXXX",
  "name": "João Silva",
  "plan": "free"
}

# Update user
PUT /api/users/{user_id}
{
  "plan": "paid",
  "is_active": true
}

# Delete user
DELETE /api/users/{user_id}
```

### Alerts Management

```bash
# List user alerts
GET /api/alerts?user_id={user_id}&skip=0&limit=100

# Create alert
POST /api/alerts?user_id={user_id}
{
  "origin_iata": "GRU",
  "destination_iata": "MIA",
  "date_from": "2026-08-01",
  "date_to": "2026-08-15",
  "max_price": 1500.0
}

# Update alert
PUT /api/alerts/{alert_id}
{
  "max_price": 1800.0,
  "is_active": false
}

# Delete alert
DELETE /api/alerts/{alert_id}
```

### Webhooks

```bash
# WhatsApp message webhook (Evolution API POSTs here)
POST /webhook/whatsapp
```

### Health Check

```bash
GET /health
GET /
```

---

## 📊 Admin Dashboard (Streamlit)

Access the admin panel at `http://localhost:8501`

### Pages

1. **🗺️ Rotas** — Add/edit/delete monitored flight routes
2. **👥 Usuários** — View users, filter by subscription plan
3. **📊 Histórico de Preços** — Charts and price history analysis
4. **📨 Alertas Enviados** — Log of all sent alerts with filters
5. **⚙️ Configurações** — Adjust scheduler intervals and price thresholds

---

## ✈️ Monitored Airlines

The bot searches across **750+ airlines** via Kiwi.com, including:

### Brazilian Carriers
- LATAM Airlines Brasil (LA)
- GOL Linhas Aéreas (G3)
- Azul Linhas Aéreas (AD)
- Voepass Linhas Aéreas (2Z)

### International Carriers
- TAP Air Portugal, Turkish Airlines, Air France, KLM, Lufthansa, British Airways, Iberia, American Airlines, Delta, United, Emirates, Qatar Airways, Aeromexico, Air Canada, Copa, Avianca, Sky Airline, JetBlue, and 700+ more

---

## 📍 Priority Routes

### Domestic (Brazil)
- GRU ↔ SSA, REC, FOR, BSB
- GIG ↔ SSA, FOR, REC
- CNF ↔ GRU, GIG

### International (Popular from Brazil)
- GRU ↔ MIA, JFK, LAX, ORD
- GRU ↔ LIS, MAD, BCN, CDG
- GRU ↔ EZE, SCL, BOG, LIM
- GRU ↔ CUN, DXB

---

## 🛠️ Development Setup (Without Docker)

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements-backend.txt
```

### 3. Set Up Database

```bash
# Run migrations
alembic upgrade head
```

### 4. Run the Bot

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Run Admin Dashboard

```bash
streamlit run streamlit_app.py
```

For Streamlit Community Cloud deployment, see `STREAMLIT_DEPLOY.md`.

If you want the Streamlit panel dependencies locally, install:

```bash
pip install -r requirements.txt
```

---

## 📂 Project Structure

```
flight-bot/
├── app/                          # Main application
│   ├── main.py                   # FastAPI app + lifespan
│   ├── config.py                 # Pydantic settings
│   ├── database.py               # SQLAlchemy async setup
│   ├── scheduler.py              # APScheduler manager
│   │
│   ├── models/                   # SQLAlchemy ORM models
│   │   ├── base.py
│   │   ├── route.py
│   │   ├── user.py
│   │   ├── alert.py
│   │   ├── price_snapshot.py
│   │   └── sent_alert.py
│   │
│   ├── schemas/                  # Pydantic request/response schemas
│   │   ├── route.py
│   │   ├── user.py
│   │   └── alert.py
│   │
│   ├── scrapers/                 # Flight price scrapers
│   │   ├── base.py               # Abstract base
│   │   └── kiwi.py               # Kiwi.com implementation
│   │
│   ├── engines/                  # Business logic
│   │   ├── price_engine.py       # Deal detection
│   │   ├── filter_engine.py      # User alert matching
│   │   └── alert_router.py       # Alert delivery
│   │
│   ├── whatsapp/                 # WhatsApp integration
│   │   ├── client.py             # Evolution API wrapper
│   │   ├── formatter.py          # Message formatting
│   │   └── commands.py           # Command parser
│   │
│   ├── routers/                  # FastAPI routes
│   │   ├── webhook.py            # WhatsApp webhook
│   │   ├── routes_api.py         # Routes CRUD
│   │   ├── users_api.py          # Users CRUD
│   │   └── alerts_api.py         # Alerts CRUD
│   │
│   └── jobs/                     # Scheduled tasks
│       ├── scan_routes.py        # Price scanning job
│       └── send_free_digest.py   # Free group digest job
│
├── admin/                        # Streamlit admin dashboard
│   └── streamlit_app.py
│
├── migrations/                   # Alembic DB migrations
│   ├── env.py
│   └── versions/
│       └── 001_initial_schema.py
│
├── .env.example                  # Environment template
├── requirements.txt              # Streamlit app dependencies
├── requirements-backend.txt      # FastAPI/backend dependencies
├── Dockerfile                    # Container image
├── docker-compose.yml            # Multi-container setup
├── alembic.ini                   # Alembic configuration
└── README.md                     # This file
```

---

## 🧪 Testing

### Test Price Scraper

```python
from app.scrapers.kiwi import KiwiScraper
from app.config import get_settings
import asyncio

async def test():
    scraper = KiwiScraper()
    flights = await scraper.search_route(
        "GRU", "MIA", "01/06/2026", "30/06/2026"
    )
    print(f"Found {len(flights)} flights")
    for flight in flights[:3]:
        print(f"{flight['origin']}->{flight['destination']}: R${flight['price']}")

asyncio.run(test())
```

### Test WhatsApp Message

```python
from app.whatsapp.client import WhatsAppClient
import asyncio

async def test():
    whatsapp = WhatsAppClient()
    success = await whatsapp.send_dm(
        "5511999999999",  # Your WhatsApp number
        "Teste de mensagem do Flight Bot ✈️"
    )
    print(f"Message sent: {success}")

asyncio.run(test())
```

---

## 📊 Database Schema

### Routes Table
Stores flight routes to monitor with price thresholds

### Users Table
WhatsApp users (free or paid)

### UserAlerts Table
Personalized price alerts created by paid users

### PriceSnapshots Table
Flight prices captured from Kiwi.com

### SentAlerts Table
Log of sent alerts for deduplication and tracking

---

## 🔐 Security Considerations

- ✅ All API keys stored in `.env` (not in code)
- ✅ Async/await prevents blocking on network calls
- ✅ Rate limiting on Kiwi.com API with exponential backoff
- ✅ Database connection pooling (async)
- ✅ Input validation via Pydantic
- 🔒 In production: enable HTTPS, add authentication, use PostgreSQL

---

## 📈 Scaling for Production

### Current Setup (Development)
- SQLite database
- Single-process scheduler
- Suitable for ~100 monitored routes

### Production Recommendations
1. **Database** → PostgreSQL with connection pooling
2. **Cache** → Dedicated Redis cluster
3. **Async** → Already implemented with async/await
4. **Monitoring** → Add Prometheus/Grafana metrics
5. **Logging** → Send logs to ELK or DataDog
6. **WhatsApp** → Use dedicated Evolution API instance or upgrade to Twilio/Z-API
7. **Deployment** → Kubernetes with horizontal pod autoscaling

---

## 🐛 Troubleshooting

### Bot not sending messages
1. Check `EVOLUTION_API_URL` and `EVOLUTION_API_KEY`
2. Verify WhatsApp instance is authenticated
3. Check bot has permission to send messages
4. Review logs: `docker-compose logs app`

### No flights found
1. Verify `KIWI_API_KEY` is valid
2. Check date format (must be DD/MM/YYYY)
3. Ensure airports exist (valid IATA codes)
4. Review logs for API errors

### Database locked (SQLite)
1. Restart bot: `docker-compose restart app`
2. For production, migrate to PostgreSQL

### Scheduler not running
1. Check logs: `docker-compose logs app`
2. Verify APScheduler started in logs
3. Restart: `docker-compose restart app`

---

## 📝 License

This project is provided as-is for personal and commercial use.

---

## 💬 Support

- Review logs: `docker-compose logs app`
- Check Evolution API status
- Verify Kiwi.com API is not rate-limited
- Test endpoints directly: `curl http://localhost:8000/health`

---

## 🚀 Future Enhancements

- [ ] Multiple WhatsApp numbers per user
- [ ] Price prediction using ML
- [ ] SMS alerts (Twilio integration)
- [ ] Telegram bot alternative
- [ ] Flexible route wildcards (GRU → Europe)
- [ ] Historical price analysis with charts
- [ ] A/B testing for alert frequency
- [ ] Integration with booking systems (flight insurance, etc.)

---

## 📧 Contact & Feedback

Have questions? Found a bug? Want to contribute?

---

**Made with ❤️ for Brazilian travelers**

✈️ Flight Bot — Never miss a flight deal again!
