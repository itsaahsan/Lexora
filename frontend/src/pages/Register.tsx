import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuthStore } from "../stores/authStore";
import api from "../lib/api";
import Button from "../components/ui/Button";
import Input from "../components/ui/Input";

export default function Register() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { setAuth } = useAuthStore();
  const navigate = useNavigate();

  useEffect(() => {
    if (useAuthStore.getState().token) {
      navigate("/dashboard", { replace: true });
      return;
    }
    // Warm up the serverless backend while the user is typing, so the
    // first POST /auth/register doesn't pay the full cold start (5-10s).
    // Fire-and-forget: failures are ignored.
    let cancelled = false;
    const warm = () => {
      if (cancelled) return;
      fetch("/health").catch(() => {});
      api.get("/health").catch(() => {});
    };
    warm();
    const t = setTimeout(warm, 2500);
    return () => {
      cancelled = true;
      clearTimeout(t);
    };
  }, [navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (loading) return;
    const trimmedEmail = email.trim();
    if (!trimmedEmail || !password) {
      setError("Email and password are required");
      return;
    }
    if (password.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const { data } = await api.post("/auth/register", {
        email: trimmedEmail,
        password,
        full_name: fullName.trim() || undefined,
      }, { timeout: 30000 });
      setAuth(data.user, data.access_token);
      navigate("/dashboard");
    } catch (err: any) {
      if (err.code === "ECONNABORTED") {
        setError("Server is waking up — please try again in a few seconds");
      } else {
        setError(err.response?.data?.detail || "Registration failed");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-4">
      <div className="glass rounded-2xl p-8 w-full max-w-md">
        <h1 className="text-2xl font-bold gradient-text text-center mb-8">
          Create Account
        </h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Full Name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            placeholder="John Doe"
          />
          <Input
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            required
          />
          <Input
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            required
          />
          {error && <p className="text-sm text-danger">{error}</p>}
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Creating account..." : "Sign Up"}
          </Button>
        </form>
        <p className="text-center text-sm text-text-muted mt-6">
          Already have an account?{" "}
          <Link to="/login" className="text-primary hover:underline">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
