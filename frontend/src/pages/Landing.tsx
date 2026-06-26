import { Link } from "react-router-dom";
import { FileText, MessageSquare, Shield, Zap } from "lucide-react";
import Button from "../components/ui/Button";

const features = [
  {
    icon: FileText,
    title: "Upload Any Document",
    desc: "Support for PDF, DOCX, TXT, MD, and CSV files with smart parsing.",
  },
  {
    icon: MessageSquare,
    title: "AI-Powered Chat",
    desc: "Ask questions about your documents and get accurate answers with citations.",
  },
  {
    icon: Shield,
    title: "Secure & Private",
    desc: "JWT authentication, encrypted storage, and role-based access control.",
  },
  {
    icon: Zap,
    title: "Lightning Fast",
    desc: "FAISS vector search delivers results in milliseconds.",
  },
];

export default function Landing() {
  return (
    <div className="min-h-screen bg-background">
      <header className="flex items-center justify-between px-8 py-6">
        <h1 className="text-2xl font-bold gradient-text">Lexora</h1>
        <div className="flex gap-3">
          <Link to="/login">
            <Button variant="ghost">Log In</Button>
          </Link>
          <Link to="/register">
            <Button>Get Started</Button>
          </Link>
        </div>
      </header>

      <section className="max-w-5xl mx-auto px-8 py-24 text-center">
        <h2 className="text-5xl font-bold mb-6">
          AI-Powered <span className="gradient-text">Document QA</span>
        </h2>
        <p className="text-xl text-text-muted mb-10 max-w-2xl mx-auto">
          Upload your documents, ask questions, and get instant answers with
          precise source citations. Built with RAG technology.
        </p>
        <div className="flex gap-4 justify-center">
          <Link to="/register">
            <Button size="lg">Start for Free</Button>
          </Link>
          <Link to="/login">
            <Button size="lg" variant="ghost">
              View Demo
            </Button>
          </Link>
        </div>
      </section>

      <section className="max-w-5xl mx-auto px-8 pb-24">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((f) => (
            <div key={f.title} className="glass rounded-2xl p-8">
              <f.icon size={32} className="text-primary mb-4" />
              <h3 className="text-lg font-semibold mb-2">{f.title}</h3>
              <p className="text-text-muted">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <footer className="text-center py-8 text-text-muted text-sm border-t border-border">
        Lexora &mdash; AI Document QA System
      </footer>
    </div>
  );
}
