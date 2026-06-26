import { useEffect, useState } from "react";
import { Users, FileText, MessageSquare, Shield } from "lucide-react";
import api from "../lib/api";
import type { User } from "../types";
import Card from "../components/ui/Card";

export default function Admin() {
  const [users, setUsers] = useState<User[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      api.get("/admin/users").then((r) => setUsers(r.data)),
      api.get("/admin/stats").then((r) => setStats(r.data)),
    ]).catch((err) => {
      setError(err.response?.data?.detail || "Failed to load admin data");
    }).finally(() => setLoading(false));
  }, []);

  const toggleActive = async (userId: string, isActive: boolean) => {
    const { data } = await api.put(`/admin/users/${userId}?is_active=${!isActive}`);
    setUsers((prev) => prev.map((u) => (u.id === userId ? { ...u, is_active: data.is_active } : u)));
  };

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">Admin Panel</h1>
      <p className="text-text-muted mb-8">System management</p>

      {loading && <div className="text-center py-12 text-text-muted">Loading...</div>}
      {error && <div className="text-center py-12 text-danger">{error}</div>}

      {!loading && !error && stats && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <Card>
            <Users size={24} className="text-primary" />
            <p className="text-2xl font-bold mt-3">{stats.total_users}</p>
            <p className="text-sm text-text-muted">Total Users</p>
          </Card>
          <Card>
            <FileText size={24} className="text-secondary" />
            <p className="text-2xl font-bold mt-3">{stats.total_documents}</p>
            <p className="text-sm text-text-muted">Documents</p>
          </Card>
          <Card>
            <MessageSquare size={24} className="text-accent" />
            <p className="text-2xl font-bold mt-3">{stats.total_conversations}</p>
            <p className="text-sm text-text-muted">Conversations</p>
          </Card>
          <Card>
            <Shield size={24} className="text-success" />
            <p className="text-2xl font-bold mt-3">{stats.active_users}</p>
            <p className="text-sm text-text-muted">Active Users</p>
          </Card>
        </div>
      )}

      <div className="glass rounded-2xl overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-border">
              <th className="text-left p-4 text-sm font-medium text-text-muted">User</th>
              <th className="text-left p-4 text-sm font-medium text-text-muted">Role</th>
              <th className="text-left p-4 text-sm font-medium text-text-muted">Status</th>
              <th className="text-right p-4 text-sm font-medium text-text-muted">Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id} className="border-b border-border last:border-0">
                <td className="p-4">
                  <p className="font-medium">{user.full_name || "N/A"}</p>
                  <p className="text-sm text-text-muted">{user.email}</p>
                </td>
                <td className="p-4 text-sm">{user.role}</td>
                <td className="p-4">
                  <span className={`text-sm ${user.is_active ? "text-success" : "text-danger"}`}>
                    {user.is_active ? "Active" : "Inactive"}
                  </span>
                </td>
                <td className="p-4 text-right">
                  <button
                    onClick={() => toggleActive(user.id, user.is_active)}
                    className="text-sm text-primary hover:underline"
                  >
                    {user.is_active ? "Deactivate" : "Activate"}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
