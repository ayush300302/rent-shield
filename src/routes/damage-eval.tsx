import { useState } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import { Loader2, ShieldAlert, ArrowLeft, Paintbrush, FileText, CheckCircle2 } from "lucide-react";
import { AppHeader } from "@/components/AppHeader";
import { evaluateDamage } from "@/lib/api/submissions";
import { toast } from "sonner";

export const Route = createFileRoute("/damage-eval")({
  head: () => ({
    meta: [
      { title: "Property Damage Evaluator — RentShield" },
      { name: "description", content: "Evaluate property damage by comparing move-in and move-out condition logs." },
    ],
  }),
  component: DamageEvalPage,
});

type DamageResult = {
  status: string;
  evaluation: {
    damage_score: number;
    damage_category: "no_damage" | "minimal" | "moderate" | "significant" | "severe";
  };
  message: string;
};

function DamageEvalPage() {
  const [beforeDesc, setBeforeDesc] = useState("");
  const [afterDesc, setAfterDesc] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DamageResult | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!beforeDesc.trim() || !afterDesc.trim()) {
      toast.error("Please fill in both condition descriptions.");
      return;
    }

    setLoading(true);
    try {
      const token = localStorage.getItem("access_token") || undefined;
      const res = await evaluateDamage(beforeDesc.trim(), afterDesc.trim(), token);
      setResult(res);
      toast.success("Damage evaluation complete!");
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Evaluation failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setBeforeDesc("");
    setAfterDesc("");
    setResult(null);
  };

  // Pre-fill helper for demonstration
  const loadSample = () => {
    setBeforeDesc("The apartment is freshly painted. All light fixtures are working, wooden flooring has no marks, and the kitchen sink plumbing has no issues.");
    setAfterDesc("Two door handles are broken. There are large coffee stains on the wooden floor and a crack in the bathroom window, but plumbing is fine.");
  };

  return (
    <div className="min-h-screen bg-canvas pb-24">
      <AppHeader />
      <main className="mx-auto max-w-2xl px-5 pt-8 md:pt-12">
        <Link
          to="/"
          className="inline-flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground transition mb-6"
        >
          <ArrowLeft className="h-3.5 w-3.5" /> Back to home
        </Link>

        <div className="flex items-center justify-between flex-wrap gap-2 text-center md:text-left">
          <div>
            <h1 className="text-3xl font-semibold tracking-tight text-foreground">
              Property Damage Evaluator
            </h1>
            <p className="mt-2 text-sm text-muted-foreground">
              Compare before/after inspections to identify damages and estimate security deposit deductions.
            </p>
          </div>
          {!result && (
            <button
              type="button"
              onClick={loadSample}
              className="text-xs font-semibold text-accent hover:underline"
            >
              Load Sample Case
            </button>
          )}
        </div>

        <div className="mt-8 rounded-3xl border border-border bg-card p-6 md:p-8 shadow-soft">
          {!result ? (
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Before Tenancy Description */}
              <label className="block">
                <span className="mb-2 block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Move-In Condition Description
                </span>
                <textarea
                  value={beforeDesc}
                  onChange={(e) => setBeforeDesc(e.target.value)}
                  placeholder="Describe the condition of walls, flooring, locks, and appliances at move-in..."
                  required
                  rows={4}
                  className="block w-full rounded-xl border border-input bg-background px-4 py-3 text-base outline-none transition focus:border-accent focus:ring-2 focus:ring-accent/20 resize-y"
                />
              </label>

              {/* After Tenancy Description */}
              <label className="block">
                <span className="mb-2 block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Move-Out Condition Description
                </span>
                <textarea
                  value={afterDesc}
                  onChange={(e) => setAfterDesc(e.target.value)}
                  placeholder="Describe any wear, breakages, or alterations noticed during move-out check..."
                  required
                  rows={4}
                  className="block w-full rounded-xl border border-input bg-background px-4 py-3 text-base outline-none transition focus:border-accent focus:ring-2 focus:ring-accent/20 resize-y"
                />
              </label>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full inline-flex h-12 items-center justify-center gap-2 rounded-full bg-foreground text-sm font-semibold text-background transition hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Running comparison...
                  </>
                ) : (
                  <>
                    <Paintbrush className="h-4 w-4" />
                    Run Damage Evaluation
                  </>
                )}
              </button>
            </form>
          ) : (
            /* Results Presentation */
            <div className="space-y-6">
              <div className="flex items-center gap-3">
                <div className="inline-flex h-10 w-10 items-center justify-center rounded-xl bg-destructive/10 text-destructive">
                  <ShieldAlert className="h-5 w-5" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold tracking-tight text-foreground">
                    Damage Report Generated
                  </h3>
                  <p className="text-xs text-muted-foreground">
                    AI-evaluated inspection logs comparison
                  </p>
                </div>
              </div>

              {/* Damage Score Visual Gauge */}
              <div className="rounded-2xl border border-border bg-canvas p-6 space-y-4">
                <div className="flex justify-between items-end">
                  <div>
                    <h4 className="text-xs font-semibold tracking-wide uppercase text-muted-foreground">
                      Damage Severity Score
                    </h4>
                    <p className="text-sm font-semibold text-foreground capitalize mt-1">
                      Category: {result.evaluation.damage_category.replace("_", " ")}
                    </p>
                  </div>
                  <div className="text-right">
                    <span className="text-4xl font-extrabold text-foreground tracking-tight">
                      {result.evaluation.damage_score}
                    </span>
                    <span className="text-sm text-muted-foreground">/9</span>
                  </div>
                </div>

                {/* Score slider indicator */}
                <div className="relative h-3 w-full rounded-full bg-secondary/80 overflow-hidden">
                  <div
                    className={`h-full transition-all duration-500 rounded-full ${
                      getCategoryColor(result.evaluation.damage_category)
                    }`}
                    style={{ width: `${(result.evaluation.damage_score / 9) * 100}%` }}
                  />
                </div>

                {/* Severity reference line */}
                <div className="flex justify-between text-[10px] text-muted-foreground font-semibold px-0.5">
                  <span>NO DAMAGE (0)</span>
                  <span>MODERATE (4)</span>
                  <span>SEVERE (9)</span>
                </div>
              </div>

              {/* Status Message */}
              <div className="rounded-2xl bg-secondary/20 p-4 border border-border/50 text-xs text-muted-foreground leading-relaxed">
                <strong>Analysis Details:</strong> {result.message}
              </div>

              {/* Button Group */}
              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={handleReset}
                  className="flex-grow inline-flex h-11 items-center justify-center rounded-full border border-border text-sm font-semibold hover:bg-secondary transition"
                >
                  Start New Comparison
                </button>
                <Link
                  to="/"
                  className="inline-flex h-11 px-6 items-center justify-center rounded-full bg-foreground text-sm font-semibold text-background hover:opacity-90 transition"
                >
                  Home
                </Link>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

function getCategoryColor(cat: string) {
  switch (cat) {
    case "no_damage":
      return "bg-success";
    case "minimal":
      return "bg-emerald-500";
    case "moderate":
      return "bg-amber-500";
    case "significant":
      return "bg-orange-500";
    case "severe":
      return "bg-destructive";
    default:
      return "bg-accent";
  }
}
