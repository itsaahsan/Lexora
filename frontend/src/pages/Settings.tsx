import { useState } from "react";
import Button from "../components/ui/Button";

export default function Settings() {
  const [darkMode, setDarkMode] = useState(true);

  return (
    <div className="max-w-xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">Settings</h1>
      <div className="glass rounded-2xl p-8 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="font-medium">Dark Mode</p>
            <p className="text-sm text-text-muted">Toggle theme appearance</p>
          </div>
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="w-12 h-6 rounded-full bg-card border border-border relative transition-colors"
          >
            <div
              className={`w-5 h-5 rounded-full bg-primary absolute top-0.5 transition-transform ${
                darkMode ? "translate-x-6" : "translate-x-0.5"
              }`}
            />
          </button>
        </div>
        <div className="border-t border-border pt-6">
          <p className="font-medium mb-2">API Configuration</p>
          <p className="text-sm text-text-muted">
            API keys are configured on the server side. Contact your admin for changes.
          </p>
        </div>
        <div className="border-t border-border pt-6">
          <p className="font-medium mb-2">Danger Zone</p>
          <Button variant="danger" size="sm">
            Delete Account
          </Button>
        </div>
      </div>
    </div>
  );
}
