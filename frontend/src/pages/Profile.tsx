import { useState } from "react";
import { useAuthStore } from "../stores/authStore";
import api from "../lib/api";
import Button from "../components/ui/Button";
import Input from "../components/ui/Input";
import Toast from "../components/ui/Toast";

export default function Profile() {
  const { user, setAuth } = useAuthStore();
  const [fullName, setFullName] = useState(user?.full_name || "");
  const [email, setEmail] = useState(user?.email || "");
  const [toast, setToast] = useState<{ message: string; type: "success" | "error" } | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const { data } = await api.put("/auth/profile", {
        full_name: fullName,
        email,
      });
      setAuth(data, useAuthStore.getState().token!);
      setToast({ message: "Profile updated", type: "success" });
    } catch (err: any) {
      setToast({ message: err.response?.data?.detail || "Update failed", type: "error" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">Profile</h1>
      <form onSubmit={handleSave} className="glass rounded-2xl p-8 space-y-4">
        <Input
          label="Full Name"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
        />
        <Input
          label="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <p className="text-sm text-text-muted">Role: {user?.role}</p>
        <Button type="submit" disabled={loading}>
          {loading ? "Saving..." : "Save Changes"}
        </Button>
      </form>
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
    </div>
  );
}
