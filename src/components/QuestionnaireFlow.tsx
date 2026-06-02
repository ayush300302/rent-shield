import { useState } from "react";
import { useServerFn } from "@tanstack/react-start";
import { useNavigate, useRouter } from "@tanstack/react-router";
import { toast } from "sonner";
import { ArrowLeft, ArrowRight, Loader2, ShieldCheck } from "lucide-react";
import { AppHeader } from "@/components/AppHeader";
import { ProgressBar } from "@/components/ProgressBar";
import { QuestionStep } from "@/components/QuestionStep";
import type { Question } from "@/lib/questionnaires";
import { submitResponse } from "@/lib/responses.functions";

type Props = {
  userType: "renter" | "owner";
  questions: Question[];
  resultTitle: string;
  resultBullets: string[];
  ctaLabel: string;
};

export function QuestionnaireFlow({
  userType,
  questions,
  resultTitle,
  resultBullets,
  ctaLabel,
}: Props) {
  const router = useRouter();
  const navigate = useNavigate();
  const submit = useServerFn(submitResponse);

  const total = questions.length;
  const [step, setStep] = useState(0); // 0..total-1 questions, total = result/lead form
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [lead, setLead] = useState({ name: "", phone: "", email: "" });
  const [submitting, setSubmitting] = useState(false);

  const onSelect = (qid: string, value: string) => {
    setAnswers((a) => ({ ...a, [qid]: value }));
    // auto-advance
    setTimeout(() => setStep((s) => Math.min(s + 1, total)), 180);
  };

  const back = () => {
    if (step === 0) router.history.back();
    else setStep((s) => s - 1);
  };

  const validateLead = () => {
    if (lead.name.trim().length < 2) return "Please enter your name";
    if (!/^[+\d\s\-()]{7,20}$/.test(lead.phone.trim())) return "Enter a valid phone number";
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(lead.email.trim())) return "Enter a valid email";
    return null;
  };

  const handleSubmit = async () => {
    const err = validateLead();
    if (err) {
      toast.error(err);
      return;
    }
    setSubmitting(true);
    try {
      await submit({
        data: {
          user_type: userType,
          answers,
          name: lead.name.trim(),
          phone: lead.phone.trim(),
          email: lead.email.trim().toLowerCase(),
        },
      });
      navigate({ to: "/thank-you" });
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Submission failed");
      setSubmitting(false);
    }
  };

  const isResult = step >= total;
  const currentQ = questions[step];
  const progressValue = isResult ? total : step + 1;

  return (
    <div className="min-h-screen bg-canvas pb-24">
      <AppHeader />
      <main className="mx-auto max-w-xl px-5 pt-8 md:pt-12">
        <div className="mb-8">
          <ProgressBar value={progressValue} total={total} />
        </div>

        {!isResult && currentQ && (
          <QuestionStep
            question={currentQ}
            value={answers[currentQ.id]}
            onSelect={(v) => onSelect(currentQ.id, v)}
          />
        )}

        {isResult && (
          <div className="space-y-8">
            <div className="rounded-3xl border border-success/30 bg-success/5 p-6 md:p-8">
              <div className="inline-flex h-10 w-10 items-center justify-center rounded-xl bg-success text-success-foreground">
                <ShieldCheck className="h-5 w-5" />
              </div>
              <h2 className="mt-5 text-2xl md:text-3xl font-semibold tracking-tight text-foreground">
                {resultTitle}
              </h2>
              <ul className="mt-4 space-y-2">
                {resultBullets.map((b) => (
                  <li
                    key={b}
                    className="flex items-start gap-2 text-sm text-muted-foreground"
                  >
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-success" />
                    <span>{b}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="space-y-4">
              <h3 className="text-lg font-semibold tracking-tight">
                Reserve your spot
              </h3>
              <Input
                label="Full name"
                value={lead.name}
                onChange={(v) => setLead({ ...lead, name: v })}
                placeholder="Your name"
              />
              <Input
                label="Mobile number"
                value={lead.phone}
                onChange={(v) => setLead({ ...lead, phone: v })}
                placeholder="+91 98xxxxxxxx"
                inputMode="tel"
              />
              <Input
                label="Email"
                value={lead.email}
                onChange={(v) => setLead({ ...lead, email: v })}
                placeholder="you@email.com"
                inputMode="email"
              />
            </div>
          </div>
        )}
      </main>

      {/* Sticky bottom bar */}
      <div className="fixed inset-x-0 bottom-0 z-20 border-t border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80">
        <div className="mx-auto flex max-w-xl items-center justify-between gap-3 px-5 py-3">
          <button
            type="button"
            onClick={back}
            className="inline-flex h-11 items-center gap-1.5 rounded-full px-4 text-sm font-medium text-muted-foreground hover:text-foreground transition"
          >
            <ArrowLeft className="h-4 w-4" />
            Back
          </button>
          {isResult ? (
            <button
              type="button"
              disabled={submitting}
              onClick={handleSubmit}
              className="inline-flex h-11 items-center gap-2 rounded-full bg-foreground px-6 text-sm font-semibold text-background transition hover:opacity-90 disabled:opacity-60"
            >
              {submitting && <Loader2 className="h-4 w-4 animate-spin" />}
              {ctaLabel}
            </button>
          ) : (
            <button
              type="button"
              disabled={!answers[currentQ?.id ?? ""]}
              onClick={() => setStep((s) => Math.min(s + 1, total))}
              className="inline-flex h-11 items-center gap-1.5 rounded-full bg-foreground px-6 text-sm font-semibold text-background transition hover:opacity-90 disabled:opacity-40"
            >
              Continue
              <ArrowRight className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

function Input({
  label,
  value,
  onChange,
  placeholder,
  inputMode,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
  inputMode?: "text" | "tel" | "email";
}) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-sm font-medium text-foreground">{label}</span>
      <input
        type="text"
        inputMode={inputMode}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="block w-full rounded-xl border border-input bg-background px-4 py-3 text-base outline-none transition focus:border-accent focus:ring-2 focus:ring-accent/20"
      />
    </label>
  );
}
