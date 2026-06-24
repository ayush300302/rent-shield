import { useState } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import { CheckCircle2, FileText, Upload, Loader2, ShieldCheck, FileCheck, HelpCircle } from "lucide-react";
import { AppHeader } from "@/components/AppHeader";
import { submitDocument } from "@/lib/api/submissions";
import { toast } from "sonner";

export const Route = createFileRoute("/thank-you")({
  head: () => ({
    meta: [{ title: "You're on the list — RentShield" }],
  }),
  component: ThankYou,
});

type DocType = "offer_letter" | "bank_account_statement";

type EvaluationResult = {
  document_type: string;
  filename?: string;
  evaluation?: Record<string, any>;
  message: string;
};

function ThankYou() {
  const [docType, setDocType] = useState<DocType>("offer_letter");
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<EvaluationResult | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selected = e.target.files[0];
      if (!selected.name.toLowerCase().endsWith(".pdf")) {
        toast.error("Only PDF files are accepted.");
        return;
      }
      setFile(selected);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      toast.error("Please select a PDF file first.");
      return;
    }

    setUploading(true);
    try {
      const token = localStorage.getItem("access_token") || undefined;
      const res = await submitDocument(docType, file, undefined, token);
      setResult(res);
      toast.success("Document evaluated successfully!");
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to evaluate document.");
    } finally {
      setUploading(false);
    }
  };

  const resetUpload = () => {
    setFile(null);
    setResult(null);
  };

  return (
    <div className="min-h-screen bg-canvas pb-24">
      <AppHeader />
      <main className="mx-auto max-w-2xl px-5 pt-12 md:pt-16">
        {/* Success Header */}
        <div className="text-center">
          <div className="mx-auto inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-success/10 text-success">
            <CheckCircle2 className="h-7 w-7" />
          </div>
          <h1 className="mt-5 text-3xl md:text-4xl font-semibold tracking-tight">
            You're on the list.
          </h1>
          <p className="mt-3 text-sm md:text-base text-muted-foreground max-w-md mx-auto">
            We will reach out with your invitation. Want to get approved faster? Verify your income documents below to fast-track your application.
          </p>
        </div>

        {/* Verification Card */}
        <div className="mt-10 rounded-3xl border border-border bg-card p-6 md:p-8 shadow-soft">
          {!result ? (
            <div className="space-y-6">
              <div>
                <h2 className="text-lg font-semibold tracking-tight text-foreground">
                  Fast-Track Verification
                </h2>
                <p className="text-xs text-muted-foreground">
                  Upload an official document to run real-time classification.
                </p>
              </div>

              {/* Document Type Selector */}
              <div className="flex gap-2 rounded-xl bg-secondary/40 p-1">
                {(
                  [
                    { id: "offer_letter", label: "Job Offer Letter" },
                    { id: "bank_account_statement", label: "Bank Statement" },
                  ] as const
                ).map((t) => (
                  <button
                    key={t.id}
                    type="button"
                    onClick={() => {
                      setDocType(t.id);
                      setFile(null);
                    }}
                    className={`flex-1 rounded-lg py-2 text-xs font-semibold tracking-tight transition ${
                      docType === t.id
                        ? "bg-background text-foreground shadow-sm"
                        : "text-muted-foreground hover:text-foreground"
                    }`}
                  >
                    {t.label}
                  </button>
                ))}
              </div>

              {/* File Upload Zone */}
              <label className="relative flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-border hover:border-accent bg-secondary/10 px-6 py-10 text-center cursor-pointer transition">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileChange}
                  className="sr-only"
                  disabled={uploading}
                />
                {file ? (
                  <div className="space-y-2">
                    <FileText className="mx-auto h-10 w-10 text-accent" />
                    <p className="text-sm font-semibold text-foreground truncate max-w-xs md:max-w-md mx-auto">
                      {file.name}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {(file.size / 1024).toFixed(1)} KB · Click to change file
                    </p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <Upload className="mx-auto h-10 w-10 text-muted-foreground group-hover:text-accent" />
                    <p className="text-sm font-semibold text-foreground">
                      Click to choose a PDF
                    </p>
                    <p className="text-xs text-muted-foreground">
                      Upload your official PDF document (under 5MB)
                    </p>
                  </div>
                )}
              </label>

              {/* Action Button */}
              <button
                type="button"
                onClick={handleUpload}
                disabled={uploading || !file}
                className="w-full inline-flex h-12 items-center justify-center gap-2 rounded-full bg-foreground text-sm font-semibold text-background transition hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {uploading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Evaluating document...
                  </>
                ) : (
                  <>
                    <ShieldCheck className="h-4 w-4" />
                    Run Verification
                  </>
                )}
              </button>
            </div>
          ) : (
            /* Results Presentation */
            <div className="space-y-6">
              <div className="flex items-center gap-3">
                <div className="inline-flex h-10 w-10 items-center justify-center rounded-xl bg-success/15 text-success">
                  <FileCheck className="h-5 w-5" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold tracking-tight text-foreground">
                    Verification Complete
                  </h3>
                  <p className="text-xs text-muted-foreground">
                    Document: {result.filename || "Uploaded file"}
                  </p>
                </div>
              </div>

              {/* Tiers display */}
              <div className="rounded-2xl bg-secondary/20 p-4 border border-border/50 space-y-4">
                <h4 className="text-xs font-semibold tracking-wide uppercase text-muted-foreground">
                  Evaluation Report
                </h4>
                {result.document_type === "offer_letter" ? (
                  <div className="grid grid-cols-2 gap-4">
                    <TierMetric
                      title="Company Classification"
                      value={result.evaluation?.company_tier}
                      labels={["MAANG / Tier 1", "Mid-sized / Tier 2", "Small/Local / Tier 3"]}
                    />
                    <TierMetric
                      title="Salary Verification"
                      value={result.evaluation?.salary_tier}
                      labels={[">10 LPA (Tier 1)", "4-10 LPA (Tier 2)", "<4 LPA (Tier 3)"]}
                    />
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <TierMetric
                      title="Account Age"
                      value={result.evaluation?.account_age_tier}
                      labels={[">3 years (Tier 1)", "1-3 years (Tier 2)", "<1 year (Tier 3)"]}
                    />
                    <TierMetric
                      title="Txn Frequency"
                      value={result.evaluation?.transaction_frequency_tier}
                      labels={[">20/mo (Tier 1)", "5-20/mo (Tier 2)", "<5/mo (Tier 3)"]}
                    />
                    <TierMetric
                      title="Volume Tiers"
                      value={result.evaluation?.transaction_volume_tier}
                      labels={[">₹1L/mo (Tier 1)", "₹25k-1L (Tier 2)", "<₹25k (Tier 3)"]}
                    />
                  </div>
                )}
                <p className="mt-3 text-xs text-muted-foreground leading-relaxed">
                  <strong>Status Message:</strong> {result.message}
                </p>
              </div>

              {/* Reset / Go back buttons */}
              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={resetUpload}
                  className="flex-1 inline-flex h-11 items-center justify-center rounded-full border border-border text-sm font-semibold hover:bg-secondary transition"
                >
                  Verify Another File
                </button>
                <Link
                  to="/"
                  className="flex-1 inline-flex h-11 items-center justify-center rounded-full bg-foreground text-sm font-semibold text-background hover:opacity-90 transition"
                >
                  Back to home
                </Link>
              </div>
            </div>
          )}
        </div>

        <div className="mt-8 text-center">
          <Link
            to="/"
            className="text-xs text-muted-foreground hover:text-foreground transition underline underline-offset-4"
          >
            Skip verification for now
          </Link>
        </div>
      </main>
    </div>
  );
}

function TierMetric({
  title,
  value,
  labels,
}: {
  title: string;
  value?: number;
  labels: [string, string, string];
}) {
  const score = value ?? 3; // default to lowest if undefined

  const colors = [
    "bg-success text-success-foreground border-success/30",
    "bg-amber-500/10 text-amber-500 border-amber-500/20",
    "bg-destructive/10 text-destructive border-destructive/20",
  ];

  const colorClass = colors[score - 1] || colors[2];
  const labelText = labels[score - 1] || "Unknown Tier";

  return (
    <div className="rounded-xl border border-border bg-card p-4 space-y-2">
      <div className="text-xs font-medium text-muted-foreground leading-none">{title}</div>
      <div className="flex items-center gap-2">
        <span
          className={`inline-flex rounded-lg px-2.5 py-1 text-xs font-bold uppercase border tracking-tight ${colorClass}`}
        >
          Tier {score}
        </span>
      </div>
      <div className="text-xs text-muted-foreground font-semibold">{labelText}</div>
    </div>
  );
}
