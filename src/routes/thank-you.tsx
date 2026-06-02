import { createFileRoute, Link } from "@tanstack/react-router";
import { CheckCircle2 } from "lucide-react";
import { AppHeader } from "@/components/AppHeader";

export const Route = createFileRoute("/thank-you")({
  head: () => ({
    meta: [{ title: "You're on the list — RentShield" }],
  }),
  component: ThankYou,
});

function ThankYou() {
  return (
    <div className="min-h-screen bg-canvas">
      <AppHeader />
      <main className="mx-auto max-w-lg px-5 pt-20 text-center">
        <div className="mx-auto inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-success/10 text-success">
          <CheckCircle2 className="h-7 w-7" />
        </div>
        <h1 className="mt-6 text-3xl md:text-4xl font-semibold tracking-tight">
          You're on the list.
        </h1>
        <p className="mt-3 text-muted-foreground">
          We'll reach out within 48 hours with your invitation. In the meantime, feel
          free to share RentShield with anyone navigating high deposits.
        </p>
        <Link
          to="/"
          className="mt-8 inline-flex h-11 items-center rounded-full bg-foreground px-6 text-sm font-semibold text-background transition hover:opacity-90"
        >
          Back to home
        </Link>
      </main>
    </div>
  );
}
