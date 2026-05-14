import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { DealsExplorer } from './pages/DealsExplorer';
import { FilterLab } from './pages/FilterLab';
import { UsersManager } from './pages/UsersManager';
import { AlertsManager } from './pages/AlertsManager';
import { RoutesManager } from './pages/RoutesManager';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/deals" element={<DealsExplorer />} />
        <Route path="/filter-lab" element={<FilterLab />} />
        <Route path="/users" element={<UsersManager />} />
        <Route path="/alerts" element={<AlertsManager />} />
        <Route path="/routes" element={<RoutesManager />} />
        <Route path="/" element={<Navigate to="/deals" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
