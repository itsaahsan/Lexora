import { useState, useCallback, useRef } from "react";
import { Upload as UploadIcon, CheckCircle, XCircle } from "lucide-react";
import api from "../lib/api";

interface UploadResult {
  filename: string;
  status: "success" | "error";
  message: string;
}

export default function Upload() {
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [results, setResults] = useState<UploadResult[]>([]);
  const handleFilesRef = useRef<(files: FileList) => Promise<void>>(null);

  const MAX_SIZE = 50 * 1024 * 1024;

  const handleFiles = async (files: FileList) => {
    setUploading(true);
    const newResults: UploadResult[] = [];

    for (const file of Array.from(files)) {
      if (file.size > MAX_SIZE) {
        newResults.push({
          filename: file.name,
          status: "error",
          message: `File too large (${(file.size / 1024 / 1024).toFixed(1)}MB). Max 50MB.`,
        });
        continue;
      }
      const formData = new FormData();
      formData.append("file", file);
      try {
        const { data } = await api.post("/documents/upload", formData);
        if (data.status === "failed") {
          newResults.push({
            filename: file.name,
            status: "error",
            message: "Processing failed. Check file content and try again.",
          });
        } else {
          newResults.push({
            filename: file.name,
            status: "success",
            message: `${data.chunk_count} chunks created`,
          });
        }
      } catch (err: any) {
        newResults.push({
          filename: file.name,
          status: "error",
          message: err.response?.data?.detail || "Upload failed",
        });
      }
    }

    setResults((prev) => [...newResults, ...prev]);
    setUploading(false);
  };

  handleFilesRef.current = handleFiles;

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files) handleFilesRef.current?.(e.dataTransfer.files);
  }, []);

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">Upload Documents</h1>
      <p className="text-text-muted mb-8">Support PDF, DOCX, TXT, MD, CSV</p>

      <div
        onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
        className={`glass rounded-2xl p-12 text-center cursor-pointer transition-all ${
          dragActive ? "border-primary border-2 bg-primary/5" : "hover:bg-card-hover"
        }`}
        onClick={() => document.getElementById("file-input")?.click()}
      >
        <UploadIcon size={48} className="mx-auto text-text-muted mb-4" />
        <p className="text-lg font-medium mb-2">
          {uploading ? "Uploading..." : "Drop files here or click to browse"}
        </p>
        <p className="text-sm text-text-muted">Max file size: 50MB</p>
        <input
          id="file-input"
          type="file"
          multiple
          accept=".pdf,.docx,.txt,.md,.csv"
          className="hidden"
          onChange={(e) => e.target.files && handleFiles(e.target.files)}
        />
      </div>

      {results.length > 0 && (
        <div className="mt-8 space-y-3">
          <h3 className="font-semibold">Upload Results</h3>
          {results.map((r, i) => (
            <div key={i} className="glass rounded-xl p-4 flex items-center gap-3">
              {r.status === "success" ? (
                <CheckCircle size={20} className="text-success" />
              ) : (
                <XCircle size={20} className="text-danger" />
              )}
              <div>
                <p className="font-medium">{r.filename}</p>
                <p className="text-sm text-text-muted">{r.message}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
