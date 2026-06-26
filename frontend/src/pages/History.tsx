import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Clock, MessageSquare, Trash2 } from "lucide-react";
import api from "../lib/api";
import type { Conversation } from "../types";
import { formatDate } from "../lib/utils";

export default function History() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    api.get("/conversations").then((r) => {
      setConversations(r.data.conversations);
      setLoading(false);
    });
  }, []);

  const handleDelete = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm("Delete this conversation?")) return;
    await api.delete(`/conversations/${id}`);
    setConversations((prev) => prev.filter((c) => c.id !== id));
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">Chat History</h1>
      <p className="text-text-muted mb-8">Your past conversations</p>

      {loading ? (
        <div className="text-center py-12 text-text-muted">Loading...</div>
      ) : conversations.length === 0 ? (
        <div className="text-center py-12 glass rounded-2xl">
          <Clock size={48} className="mx-auto text-text-muted mb-4" />
          <p className="text-lg">No conversations yet</p>
        </div>
      ) : (
        <div className="space-y-3">
          {conversations.map((conv) => (
            <div
              key={conv.id}
              onClick={() => navigate("/chat")}
              className="glass rounded-xl p-4 flex items-center justify-between cursor-pointer hover:bg-card-hover transition-colors"
            >
              <div className="flex items-center gap-4">
                <MessageSquare size={20} className="text-primary" />
                <div>
                  <p className="font-medium">{conv.title}</p>
                  <p className="text-sm text-text-muted">{formatDate(conv.created_at)}</p>
                </div>
              </div>
              <button
                onClick={(e) => handleDelete(conv.id, e)}
                className="text-text-muted hover:text-danger transition-colors"
              >
                <Trash2 size={18} />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
