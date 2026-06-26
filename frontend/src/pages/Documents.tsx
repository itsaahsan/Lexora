import { useEffect, useState } from "react";
import { FileText, Trash2, RefreshCw } from "lucide-react";
import api from "../lib/api";
import type { Document } from "../types";
import { formatDate, formatFileSize } from "../lib/utils";
import Button from "../components/ui/Button";

export default function Documents() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchDocuments = async () => {
    setLoading(true);
    try {
      const { data } = await api.get("/documents");
      setDocuments(data.documents);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchDocuments(); }, []);

  const handleDelete = async (id: string) => {
    if (!confirm("Delete this document?")) return;
    try {
      await api.delete(`/documents/${id}`);
      setDocuments((prev) => prev.filter((d) => d.id !== id));
    } catch {}
  };

  const statusColors: Record<string, string> = {
    ready: "text-success",
    processing: "text-accent",
    failed: "text-danger",
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold">Documents</h1>
          <p className="text-text-muted">Manage your uploaded documents</p>
        </div>
        <Button onClick={fetchDocuments} variant="ghost" size="sm">
          <RefreshCw size={16} className="mr-2" /> Refresh
        </Button>
      </div>

      {loading ? (
        <div className="text-center py-12 text-text-muted">Loading...</div>
      ) : documents.length === 0 ? (
        <div className="text-center py-12 glass rounded-2xl">
          <FileText size={48} className="mx-auto text-text-muted mb-4" />
          <p className="text-lg">No documents uploaded yet</p>
        </div>
      ) : (
        <div className="space-y-3">
          {documents.map((doc) => (
            <div key={doc.id} className="glass rounded-xl p-4 flex items-center justify-between">
              <div className="flex items-center gap-4">
                <FileText size={24} className="text-primary" />
                <div>
                  <p className="font-medium">{doc.filename}</p>
                  <p className="text-sm text-text-muted">
                    {formatFileSize(doc.file_size)} &middot; {doc.chunk_count} chunks &middot;{" "}
                    <span className={statusColors[doc.status] || "text-text-muted"}>
                      {doc.status}
                    </span>
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <span className="text-xs text-text-muted">{formatDate(doc.created_at)}</span>
                <button
                  onClick={() => handleDelete(doc.id)}
                  className="text-text-muted hover:text-danger transition-colors"
                >
                  <Trash2 size={18} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
