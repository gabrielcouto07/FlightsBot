import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { DealsExplorer } from './pages/DealsExplorer';
import { FilterLab } from './pages/FilterLab';
import { AlertsLab } from './pages/AlertsLab';
import { RouteMonitor } from './pages/RouteMonitor';
import { UsersManager } from './pages/UsersManager';
import { AlertsManager } from './pages/AlertsManager';
import { RoutesManager } from './pages/RoutesManager';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<DealsExplorer />} />
        <Route path="/deals" element={<Navigate to="/" replace />} />
        <Route path="/alerts-lab" element={<AlertsLab />} />
        <Route path="/route-monitor" element={<RouteMonitor />} />
        <Route path="/filter-lab" element={<FilterLab />} />
        <Route path="/users" element={<UsersManager />} />
        <Route path="/alerts" element={<Navigate to="/alerts-lab" replace />} />
        <Route path="/routes" element={<Navigate to="/route-monitor" replace />} />
        <Route path="/legacy-alerts" element={<AlertsManager />} />
        <Route path="/legacy-routes" element={<RoutesManager />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
