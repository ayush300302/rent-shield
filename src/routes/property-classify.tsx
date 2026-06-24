import { useState } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import { Loader2, ShieldAlert, ArrowLeft, Building2, MapPin, BadgePercent, Coins } from "lucide-react";
import { AppHeader } from "@/components/AppHeader";
import { classifyProperty } from "@/lib/api/submissions";
import { toast } from "sonner";

export const Route = createFileRoute("/property-classify")({
  head: () => ({
    meta: [
      { title: "Property Tier Classifier — RentShield" },
      { name: "description", content: "Classify your rental property location, rent, and deposit risks." },
    ],
  }),
  component: PropertyClassifyPage,
});

type ClassificationResult = {
  status: string;
  evaluation: {
    location: number;
    rent: number;
    deposit_neededd: number;
  };
  message: string;
};

function PropertyClassifyPage() {
  const [location, setLocation] = useState("");
  const [rent, setRent] = useState("");
  const [deposit, setDeposit] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ClassificationResult | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!location.trim()) {
      toast.error("Please enter a city or location.");
      return;
    }
    const rentVal = parseFloat(rent);
    const depositVal = parseFloat(deposit);
    if (isNaN(rentVal) || rentVal <= 0) {
      toast.error("Please enter a valid monthly rent.");
      return;
    }
    if (isNaN(depositVal) || depositVal < 0) {
      toast.error("Please enter a valid deposit amount.");
      return;
    }

    setLoading(true);
    try {
      const token = localStorage.getItem("access_token") || undefined;
      const res = await classifyProperty(location.trim(), rentVal, depositVal, token);
      setResult(res);
      toast.success("Property classified successfully!");
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Classification failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setLocation("");
    setRent("");
    setDeposit("");
    setResult(null);
  };

  return (
    <div className="min-h-screen bg-canvas pb-24">
      <AppHeader />
      <main className="mx-auto max-w-xl px-5 pt-8 md:pt-12">
        <Link
          to="/"
          className="inline-flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground transition mb-6"
        >
          <ArrowLeft className="h-3.5 w-3.5" /> Back to home
        </Link>

        <div className="text-center md:text-left">
          <h1 className="text-3xl font-semibold tracking-tight text-foreground">
            Property Tier Classifier
          </h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Analyze location density, monthly rent brackets, and upfront deposit security tiers to understand deposit insurance eligibility.
          </p>
        </div>

        <div className="mt-8 rounded-3xl border border-border bg-card p-6 md:p-8 shadow-soft">
          {!result ? (
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Location Input */}
              <label className="block">
                <span className="mb-2 block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Location (City or State)
                </span>
                <div className="relative">
                  <MapPin className="absolute left-3.5 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
                  <input
                    type="text"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    placeholder="e.g., Bengaluru, Maharashtra"
                    required
                    className="block w-full rounded-xl border border-input bg-background pl-11 pr-4 py-3 text-base outline-none transition focus:border-accent focus:ring-2 focus:ring-accent/20"
                  />
                </div>
              </label>

              {/* Monthly Rent Input */}
              <label className="block">
                <span className="mb-2 block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Monthly Rent (INR)
                </span>
                <div className="relative">
                  <Coins className="absolute left-3.5 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
                  <input
                    type="number"
                    value={rent}
                    onChange={(e) => setRent(e.target.value)}
                    placeholder="e.g., 35000"
                    required
                    min="1"
                    className="block w-full rounded-xl border border-input bg-background pl-11 pr-4 py-3 text-base outline-none transition focus:border-accent focus:ring-2 focus:ring-accent/20"
                  />
                </div>
              </label>

              {/* Deposit Months Input */}
              <label className="block">
                <span className="mb-2 block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Security Deposit (Months Requested)
                </span>
                <div className="relative">
                  <BadgePercent className="absolute left-3.5 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
                  <input
                    type="number"
                    value={deposit}
                    onChange={(e) => setDeposit(e.target.value)}
                    placeholder="e.g., 6"
                    required
                    min="0"
                    className="block w-full rounded-xl border border-input bg-background pl-11 pr-4 py-3 text-base outline-none transition focus:border-accent focus:ring-2 focus:ring-accent/20"
                  />
                </div>
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
                    Analyzing property...
                  </>
                ) : (
                  <>
                    <Building2 className="h-4 w-4" />
                    Classify Property
                  </>
                )}
              </button>
            </form>
          ) : (
            /* Results Presentation */
            <div className="space-y-6">
              <div className="flex items-center gap-3">
                <div className="inline-flex h-10 w-10 items-center justify-center rounded-xl bg-accent/10 text-accent">
                  <Building2 className="h-5 w-5" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold tracking-tight text-foreground">
                    Classification Result
                  </h3>
                  <p className="text-xs text-muted-foreground">
                    Location: {location} · Rent: ₹{parseFloat(rent).toLocaleString()}
                  </p>
                </div>
              </div>

              {/* Metrics Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <ClassifyMetric
                  title="Location Density"
                  value={result.evaluation.location}
                  descriptions={["Metro/High Tier", "Tier 2 City", "Rural/Tier 3"]}
                />
                <ClassifyMetric
                  title="Rent Bracket"
                  value={result.evaluation.rent}
                  descriptions={[">₹50k (High)", "₹15k-50k (Medium)", "<₹15k (Low)"]}
                />
                <ClassifyMetric
                  title="Deposit Risk"
                  value={result.evaluation.deposit_neededd}
                  descriptions={["1 Month (Low Risk)", "2-3 Months (Med Risk)", ">3 Months (High Risk)"]}
                />
              </div>

              {/* Status Message */}
              <div className="rounded-2xl bg-secondary/20 p-4 border border-border/50 text-xs text-muted-foreground leading-relaxed">
                <strong>Analysis summary:</strong> {result.message}
              </div>

              {/* Button Group */}
              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={handleReset}
                  className="flex-grow inline-flex h-11 items-center justify-center rounded-full border border-border text-sm font-semibold hover:bg-secondary transition"
                >
                  Classify New Property
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

function ClassifyMetric({
  title,
  value,
  descriptions,
}: {
  title: string;
  value: number;
  descriptions: [string, string, string];
}) {
  const colors = [
    "bg-success text-success-foreground border-success/30",
    "bg-amber-500/10 text-amber-500 border-amber-500/20",
    "bg-destructive/10 text-destructive border-destructive/20",
  ];

  const colorClass = colors[value - 1] || colors[2];
  const descText = descriptions[value - 1] || "Unknown Tier";

  return (
    <div className="rounded-xl border border-border bg-card p-4 space-y-2">
      <div className="text-xs font-medium text-muted-foreground leading-none">{title}</div>
      <div className="flex items-center gap-2">
        <span
          className={`inline-flex rounded-lg px-2.5 py-1 text-xs font-bold uppercase border tracking-tight ${colorClass}`}
        >
          Tier {value}
        </span>
      </div>
      <div className="text-xs text-muted-foreground font-semibold">{descText}</div>
    </div>
  );
}
