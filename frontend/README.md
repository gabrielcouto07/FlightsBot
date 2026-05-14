# Flight Bot - Frontend Demo Application

A modern, investor-ready React web application for discovering flight deals in real-time. Features a dark theme inspired by Linear.app with comprehensive deal exploration and user management capabilities.

## 🚀 Features

### Deal Explorer
- Real-time flight search across 750+ airlines
- Intelligent deal detection and pricing tiers
- Airline logos and flight details visualization
- Live match preview showing which deals match user alerts

### User Management
- CRUD operations for test users
- Free vs Paid plan differentiation
- User alert tracking and management

### Alert & Route Managers
- View and manage flight price alerts
- Route configuration with price thresholds
- Active/inactive status tracking

### Filter Lab
- Test matching logic between deals and user alerts
- Experiment with search filters
- Real-time feedback on deal-alert relationships

## 🛠️ Tech Stack

- **Frontend Framework**: React 18
- **Build Tool**: Vite
- **Language**: TypeScript
- **Styling**: TailwindCSS v4 (custom dark theme)
- **UI Components**: Radix UI (headless), Lucide React icons
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Routing**: React Router v6
- **Dates**: date-fns

## 📋 Prerequisites

- Node.js 16+ (or use `nvm`)
- npm or yarn
- Backend API running at `http://localhost:8000`

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Environment
```bash
cp .env.example .env.local
# Edit .env.local if needed (API_URL defaults to localhost:8000)
```

### 3. Start Development Server
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## 📁 Project Structure

```
frontend/
├── src/
│   ├── api/                 # API clients
│   │   ├── client.ts        # Axios configuration
│   │   ├── search.ts        # Flight search API
│   │   ├── users.ts         # User management
│   │   ├── routes.ts        # Route management
│   │   ├── alerts.ts        # Alert management
│   │   └── demo.ts          # Demo seeding
│   ├── components/
│   │   ├── ui/              # Reusable UI components (9 files)
│   │   ├── layout/          # Layout components (Sidebar, TopBar)
│   │   ├── flights/         # Flight-specific components
│   │   └── users/           # User management components
│   ├── pages/               # Page components
│   ├── store/               # Zustand stores
│   ├── App.tsx              # Router setup
│   ├── main.tsx             # Entry point
│   └── index.css            # Global styles
├── public/                  # Static assets
├── package.json
├── vite.config.ts
├── tailwind.config.ts
├── tsconfig.json
└── vercel.json              # Vercel deployment config
```

## 🎨 Design System

### Color Palette
- **Background**: `#0f0f0f` (primary), `#161616` (secondary)
- **Accent**: `#00b4b4` (Teal)
- **Borders**: `#2a2a2a`, `#333333`
- **Semantic**: Green (success), Yellow (warning), Red (danger), Blue (info)

### UI Components
1. **Button** - Primary, secondary, danger, outline variants
2. **Badge** - Status indicators with multiple variants
3. **Card** - Container with hover effects
4. **Input** - Text input with labels and error states
5. **Select** - Dropdown selection
6. **Modal** - Dialog for forms and confirmations
7. **Table** - Data grid with hover interactions
8. **Skeleton** - Loading placeholders
9. **EmptyState** - Fallback UI for empty data

## 🔌 API Integration

### Available Endpoints

**Search**:
- `GET /api/search/deals` - Search flights with enrichment
- `POST /api/search/preview-match` - Preview which deals match user alerts

**Users**:
- `GET /api/users` - List all users
- `POST /api/users` - Create user
- `GET /api/users/{id}` - Get user
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user

**Alerts**:
- `GET /api/alerts` - List alerts
- `POST /api/alerts` - Create alert
- `DELETE /api/alerts/{id}` - Delete alert

**Routes**:
- `GET /api/routes` - List routes
- `POST /api/routes` - Create route
- `DELETE /api/routes/{id}` - Delete route

**Demo**:
- `POST /api/demo/seed` - Seed demo data (creates 5 users, 8 routes, 4 alerts)
- `GET /api/demo/notifications` - Get demo notifications

## 📦 Build & Deploy

### Development Build
```bash
npm run dev
```

### Production Build
```bash
npm run build
npm run preview
```

### Deploy to Vercel
1. Push to GitHub
2. Connect repository to Vercel
3. Set environment variable: `VITE_API_URL=https://your-api.vercel.app`
4. Deploy!

## 🧪 Testing Features

### Filter Lab Page
Test matching logic between deals and user alerts:
1. Search for deals on the left
2. View available test users in the center
3. Run match preview to see which deals match user alerts

### Demo Data Seeding
Call the `/api/demo/seed` endpoint to populate test data:
- 5 users (3 free, 2 paid)
- 8 domestic + international routes
- 4 price alerts with varying criteria

## 🔍 Performance Optimizations

- Code splitting via Vite
- Lazy loading of pages
- Zustand for lightweight state management
- Memoized components for expensive renders
- CSS-in-JS using TailwindCSS

## 📱 Responsive Design

Fully responsive layout:
- Mobile-first approach
- Sidebar collapses on smaller screens
- Cards adapt to container width
- Touch-friendly components

## 🚨 Error Handling

- API errors caught and logged
- User-friendly error messages
- Fallback UIs for failed states
- Loading skeletons for data fetching

## 🔐 Security

- CORS-enabled API client
- Environment-based API configuration
- XSS protection via React
- Input validation on forms

## 📝 Contributing

When adding new features:
1. Create components in appropriate folders
2. Follow existing naming conventions
3. Use TypeScript for type safety
4. Document complex logic

## 📄 License

Part of Flight Bot project - MIT License

---

**Built with ❤️ for investors and flight deal enthusiasts** ✈️
