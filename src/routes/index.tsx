import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowRight, Home, KeyRound, ShieldCheck, Sparkles, TrendingDown } from "lucide-react";
import { AppHeader } from "@/components/AppHeader";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "RentShield — Rent without the deposit burden" },
      {
        name: "description",
        content:
          "RentShield protects landlords and reduces upfront deposits for renters. Check eligibility in under 60 seconds.",
      },
      { property: "og:title", content: "RentShield — Rent without the deposit burden" },
      {
        property: "og:description",
        content:
          "Insured deposit reduction for India's rental market. Built for renters and property owners.",
      },
    ],
  }),
  component: Landing,
});

function Landing() {
  return (
    <div className="min-h-screen bg-canvas">
      <AppHeader />
      <main className="mx-auto max-w-5xl px-5 pt-12 pb-24 md:pt-20">
        <section className="text-center">
          <div className="inline-flex items-center gap-2 rounded-full border border-border bg-background px-3 py-1 text-xs font-medium text-muted-foreground shadow-soft">
            <Sparkles className="h-3.5 w-3.5 text-accent" />
            Now in private beta · India
          </div>
          <h1 className="mt-6 text-4xl md:text-6xl font-semibold tracking-tight text-foreground leading-[1.05]">
            Rent without the
            <br />
            <span className="text-accent">deposit burden.</span>
          </h1>
          <p className="mx-auto mt-5 max-w-xl text-base md:text-lg text-muted-foreground">
            RentShield replaces 6-month deposits with insured protection — fairer for
            renters, safer for landlords. Check eligibility in under a minute.
          </p>
        </section>

        <section className="mt-12 md:mt-16 grid gap-4 md:grid-cols-2">
          <ChoiceCard
            to="/renter"
            icon={<KeyRound className="h-5 w-5" />}
            eyebrow="For renters"
            title="I'm a Renter"
            description="Lower your upfront deposit. Move in faster."
            accent="accent"
          />
          <ChoiceCard
            to="/owner"
            icon={<Home className="h-5 w-5" />}
            eyebrow="For property owners"
            title="I'm a Property Owner"
            description="Reduce vacancy. Insure against tenant risk."
            accent="success"
          />
        </section>

        <section className="mt-20 grid gap-8 md:grid-cols-3">
          <Feature
            icon={<TrendingDown className="h-5 w-5" />}
            title="Up to 80% lower deposit"
            text="Most renters qualify to reduce 6 months down to 1."
          />
          <Feature
            icon={<ShieldCheck className="h-5 w-5" />}
            title="Landlord-backed protection"
            text="Covers damages and missed rent up to ₹2,00,000."
          />
          <Feature
            icon={<Sparkles className="h-5 w-5" />}
            title="60-second eligibility"
            text="No paperwork. Just answer a few quick questions."
          />
        </section>
      </main>
      <footer className="border-t border-border/60 py-8 text-center text-xs text-muted-foreground">
        © {new Date().getFullYear()} RentShield · Validation pilot
      </footer>
    </div>
  );
}

function ChoiceCard({
  to,
  icon,
  eyebrow,
  title,
  description,
  accent,
}: {
  to: "/renter" | "/owner";
  icon: React.ReactNode;
  eyebrow: string;
  title: string;
  description: string;
  accent: "accent" | "success";
}) {
  const ring = accent === "accent" ? "hover:border-accent" : "hover:border-success";
  const chip =
    accent === "accent"
      ? "bg-accent/10 text-accent"
      : "bg-success/10 text-success";
  return (
    <Link
      to={to}
      className={`group relative flex flex-col rounded-3xl border border-border bg-card p-7 transition-all hover:shadow-card ${ring}`}
    >
      <div className={`inline-flex h-10 w-10 items-center justify-center rounded-xl ${chip}`}>
        {icon}
      </div>
      <div className="mt-6">
        <div className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
          {eyebrow}
        </div>
        <h3 className="mt-1 text-2xl font-semibold tracking-tight text-foreground">
          {title}
        </h3>
        <p className="mt-2 text-muted-foreground">{description}</p>
      </div>
      <div className="mt-8 flex items-center justify-between">
        <span className="text-sm font-medium text-foreground">Check eligibility</span>
        <ArrowRight className="h-5 w-5 text-foreground transition-transform group-hover:translate-x-1" />
      </div>
    </Link>
  );
}

function Feature({
  icon,
  title,
  text,
}: {
  icon: React.ReactNode;
  title: string;
  text: string;
}) {
  return (
    <div>
      <div className="inline-flex h-9 w-9 items-center justify-center rounded-lg bg-secondary text-foreground">
        {icon}
      </div>
      <h4 className="mt-4 text-base font-semibold text-foreground">{title}</h4>
      <p className="mt-1 text-sm text-muted-foreground">{text}</p>
    </div>
  );
}
