import { Link } from "@tanstack/react-router";
import { Shield } from "lucide-react";

export function AppHeader() {
  return (
    <header className="sticky top-0 z-30 border-b border-border/60 bg-background/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-5xl items-center justify-between px-5">
        <div className="flex items-center gap-6">
          <Link to="/" className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-foreground text-background">
              <Shield className="h-4 w-4" />
            </div>
            <span className="text-base font-semibold tracking-tight">RentShield</span>
          </Link>
          <nav className="hidden sm:flex items-center gap-4">
            <Link
              to="/property-classify"
              className="text-xs font-semibold text-muted-foreground hover:text-foreground transition uppercase tracking-wider"
            >
              Classifier
            </Link>
            <Link
              to="/damage-eval"
              className="text-xs font-semibold text-muted-foreground hover:text-foreground transition uppercase tracking-wider"
            >
              Evaluator
            </Link>
          </nav>
        </div>
        <Link
          to="/admin"
          className="text-sm font-semibold text-muted-foreground hover:text-foreground transition"
        >
          Admin
        </Link>
      </div>
    </header>
  );
}
