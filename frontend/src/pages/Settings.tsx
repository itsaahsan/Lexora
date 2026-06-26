import Button from "../components/ui/Button";

export default function Settings() {
  return (
    <div className="max-w-xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">Settings</h1>
      <div className="glass rounded-2xl p-8 space-y-6">
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
