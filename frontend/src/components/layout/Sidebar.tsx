import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  Upload,
  FileText,
  MessageSquare,
  Clock,
  User,
  Settings,
  Shield,
  LogOut,
} from "lucide-react";
import { useAuthStore } from "../../stores/authStore";
import { cn } from "../../lib/utils";

const navItems = [
  { to: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/upload", icon: Upload, label: "Upload" },
  { to: "/documents", icon: FileText, label: "Documents" },
  { to: "/chat", icon: MessageSquare, label: "Chat" },
  { to: "/history", icon: Clock, label: "History" },
];

const bottomItems = [
  { to: "/profile", icon: User, label: "Profile" },
  { to: "/settings", icon: Settings, label: "Settings" },
];

export default function Sidebar() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <aside className="w-64 h-screen glass flex flex-col fixed left-0 top-0 z-40">
      <div className="p-6">
        <h1 className="text-xl font-bold gradient-text">Lexora</h1>
        <p className="text-xs text-text-muted mt-1">AI Document QA</p>
      </div>

      <nav className="flex-1 px-3 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors",
                isActive
                  ? "bg-primary/20 text-primary"
                  : "text-text-muted hover:text-text hover:bg-card-hover"
              )
            }
          >
            <item.icon size={18} />
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="px-3 pb-3 space-y-1">
        {user?.role === "admin" && (
          <NavLink
            to="/admin"
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors",
                isActive
                  ? "bg-primary/20 text-primary"
                  : "text-text-muted hover:text-text hover:bg-card-hover"
              )
            }
          >
            <Shield size={18} />
            Admin
          </NavLink>
        )}
        {bottomItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors",
                isActive
                  ? "bg-primary/20 text-primary"
                  : "text-text-muted hover:text-text hover:bg-card-hover"
              )
            }
          >
            <item.icon size={18} />
            {item.label}
          </NavLink>
        ))}
        <button
          onClick={handleLogout}
          className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-text-muted hover:text-danger hover:bg-card-hover w-full transition-colors"
        >
          <LogOut size={18} />
          Logout
        </button>
      </div>

      <div className="p-4 border-t border-border">
        <p className="text-sm font-medium truncate">{user?.full_name || user?.email}</p>
        <p className="text-xs text-text-muted truncate">{user?.email}</p>
      </div>
    </aside>
  );
}
