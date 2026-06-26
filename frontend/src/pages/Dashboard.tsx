import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { FileText, MessageSquare, Database, Layers } from "lucide-react";
import api from "../lib/api";
import type { Analytics } from "../types";
import Card from "../components/ui/Card";

export default function Dashboard() {
  const [analytics, setAnalytics] = useState<Analytics | null>(null);

  useEffect(() => {
    api.get("/analytics/overview").then((r) => setAnalytics(r.data));
  }, []);

  const stats = [
    { label: "Documents", value: analytics?.total_documents ?? 0, icon: FileText, color: "text-primary" },
    { label: "Conversations", value: analytics?.total_conversations ?? 0, icon: MessageSquare, color: "text-secondary" },
    { label: "Messages", value: analytics?.total_messages ?? 0, icon: Database, color: "text-accent" },
    { label: "Chunks Indexed", value: analytics?.total_chunks ?? 0, icon: Layers, color: "text-success" },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
      <p className="text-text-muted mb-8">Overview of your document QA system</p>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {stats.map((s) => (
          <Card key={s.label}>
            <s.icon size={24} className={s.color} />
            <p className="text-2xl font-bold mt-3">{s.value}</p>
            <p className="text-sm text-text-muted">{s.label}</p>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Link to="/upload" className="glass rounded-2xl p-6 hover:bg-card-hover transition-colors">
          <h3 className="text-lg font-semibold mb-2">Upload Documents</h3>
          <p className="text-text-muted text-sm">Add new documents to your knowledge base</p>
        </Link>
        <Link to="/chat" className="glass rounded-2xl p-6 hover:bg-card-hover transition-colors">
          <h3 className="text-lg font-semibold mb-2">Start Chatting</h3>
          <p className="text-text-muted text-sm">Ask questions about your documents</p>
        </Link>
      </div>
    </div>
  );
}
