import type { Question } from "@/lib/questionnaires";
import { Check } from "lucide-react";

type Props = {
  question: Question;
  value: string | undefined;
  onSelect: (v: string) => void;
};

export function QuestionStep({ question, value, onSelect }: Props) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl md:text-3xl font-semibold tracking-tight text-foreground">
          {question.title}
        </h2>
        {question.subtitle && (
          <p className="mt-2 text-muted-foreground">{question.subtitle}</p>
        )}
      </div>
      <div className="grid gap-3">
        {question.options.map((o) => {
          const selected = value === o.value;
          return (
            <button
              key={o.value}
              type="button"
              onClick={() => onSelect(o.value)}
              className={[
                "group flex items-center justify-between text-left rounded-2xl border bg-card px-5 py-4 transition-all",
                "hover:border-accent hover:shadow-soft",
                selected
                  ? "border-accent ring-2 ring-accent/20 shadow-soft"
                  : "border-border",
              ].join(" ")}
            >
              <span className="text-base font-medium text-foreground">
                {o.label}
              </span>
              <span
                className={[
                  "flex h-6 w-6 items-center justify-center rounded-full border transition",
                  selected
                    ? "bg-accent border-accent text-accent-foreground"
                    : "border-border text-transparent group-hover:border-accent/40",
                ].join(" ")}
              >
                <Check className="h-4 w-4" />
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
