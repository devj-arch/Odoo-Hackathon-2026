import { Navigate, Route, Routes } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute.jsx";
import ForgotPasswordPage from "./pages/ForgotPasswordPage.jsx";
import HomePage from "./pages/HomePage.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import ResetPasswordPage from "./pages/ResetPasswordPage.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import VehicleRegistry from "./pages/VehicleRegistry.jsx";
import DriverManagement from "./pages/DriverManagement.jsx";
import TripDispatcher from "./pages/TripDispatcher.jsx";
import MaintenanceLog from "./pages/MaintenanceLog.jsx";
import FuelExpenseManagement from "./pages/FuelExpenseManagement.jsx";
import Reports from "./pages/Reports.jsx";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/forgot-password" element={<ForgotPasswordPage />} />
      <Route path="/reset-password" element={<ResetPasswordPage />} />

      <Route element={<ProtectedRoute />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/vehicles" element={<VehicleRegistry />} />
        <Route path="/drivers" element={<DriverManagement />} />
        <Route path="/trips" element={<TripDispatcher />} />
        <Route path="/maintenance" element={<MaintenanceLog />} />
        <Route path="/fuel-expenses" element={<FuelExpenseManagement />} />
        <Route path="/reports" element={<Reports />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;