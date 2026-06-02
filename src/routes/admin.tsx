import { useEffect, useMemo, useState } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { useServerFn } from "@tanstack/react-start";
import * as XLSX from "xlsx";
import { Loader2, LogOut, Download, Search, ShieldCheck } from "lucide-react";
import { toast } from "sonner";
import { supabase } from "@/integrations/supabase/client";
import { listResponses, checkIsAdmin } from "@/lib/admin.functions";
import { AppHeader } from "@/components/AppHeader";

export const Route = createFileRoute("/admin")({
  ssr: false,
  head: () => ({ meta: [{ title: "Admin — RentShield" }] }),
  component: AdminPage,
});

type AuthState =
  | { status: "loading" }
  | { status: "signed_out" }
  | { status: "not_admin"; email: string }
  | { status: "admin"; email: string };

function AdminPage() {
  const [auth, setAuth] = useState<AuthState>({ status: "loading" });
  const checkAdmin = useServerFn(checkIsAdmin);

  const resolveAuth = async () => {
    const { data } = await supabase.auth.getUser();
    if (!data.user) {
      setAuth({ status: "signed_out" });
      return;
    }
    try {
      const res = await checkAdmin();
      setAuth(
        res.isAdmin
          ? { status: "admin", email: data.user.email ?? "" }
          : { status: "not_admin", email: data.user.email ?? "" },
      );
    } catch {
      setAuth({ status: "not_admin", email: data.user.email ?? "" });
    }
  };

  useEffect(() => {
    void resolveAuth();
    const { data: sub } = supabase.auth.onAuthStateChange(() => {
      void resolveAuth();
    });
    return () => sub.subscription.unsubscribe();
  }, []);

  return (
    <div className="min-h-screen bg-canvas">
      <AppHeader />
      {auth.status === "loading" && <CenteredLoader />}
      {auth.status === "signed_out" && <LoginCard />}
      {auth.status === "not_admin" && (
        <NotAdminCard
          email={auth.email}
          onSignOut={async () => {
            await supabase.auth.signOut();
          }}
        />
      )}
      {auth.status === "admin" && <Dashboard email={auth.email} />}
    </div>
  );
}

function CenteredLoader() {
  return (
    <div className="flex h-[60vh] items-center justify-center">
      <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
    </div>
  );
}

const ADMIN_EMAIL = "kv@rentshield.local";

function LoginCard() {
  const [email, setEmail] = useState(ADMIN_EMAIL);
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    try {
      const { error } = await supabase.auth.signInWithPassword({
        email: email.trim(),
        password,
      });
      if (error) throw error;
      toast.success("Signed in");
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Authentication failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <main className="mx-auto max-w-md px-5 pt-16">
      <div className="rounded-3xl border border-border bg-card p-8 shadow-soft">
        <div className="inline-flex h-10 w-10 items-center justify-center rounded-xl bg-foreground text-background">
          <ShieldCheck className="h-5 w-5" />
        </div>
        <h1 className="mt-5 text-2xl font-semibold tracking-tight">Admin access</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Sign in to view responses.
        </p>
        <form className="mt-6 space-y-4" onSubmit={onSubmit}>
          <AuthInput
            label="Email"
            type="email"
            value={email}
            onChange={setEmail}
            placeholder={ADMIN_EMAIL}
            required
          />
          <AuthInput
            label="Password"
            type="password"
            value={password}
            onChange={setPassword}
            placeholder="••••••••"
            required
          />
          <button
            type="submit"
            disabled={busy}
            className="inline-flex h-11 w-full items-center justify-center gap-2 rounded-full bg-foreground text-sm font-semibold text-background transition hover:opacity-90 disabled:opacity-60"
          >
            {busy && <Loader2 className="h-4 w-4 animate-spin" />}
            Sign in
          </button>
        </form>
      </div>
    </main>
  );
}

function NotAdminCard({ email, onSignOut }: { email: string; onSignOut: () => Promise<void> }) {
  return (
    <main className="mx-auto max-w-md px-5 pt-16 text-center">
      <div className="rounded-3xl border border-border bg-card p-8 shadow-soft">
        <h1 className="text-xl font-semibold tracking-tight">Access pending</h1>
        <p className="mt-2 text-sm text-muted-foreground">
          You're signed in as <span className="font-medium text-foreground">{email}</span>, but
          this account doesn't have admin access yet.
        </p>
        <button
          type="button"
          onClick={onSignOut}
          className="mt-6 inline-flex h-10 items-center gap-2 rounded-full border border-border bg-background px-5 text-sm font-medium text-foreground transition hover:bg-secondary"
        >
          <LogOut className="h-4 w-4" /> Sign out
        </button>
      </div>
    </main>
  );
}

type Row = {
  id: string;
  created_at: string;
  user_type: "renter" | "owner";
  answers: Record<string, string>;
  name: string;
  phone: string;
  email: string;
  city: string | null;
  status: string;
};

function Dashboard({ email }: { email: string }) {
  const list = useServerFn(listResponses);
  const [rows, setRows] = useState<Row[] | null>(null);
  const [filter, setFilter] = useState<"all" | "renter" | "owner">("all");
  const [q, setQ] = useState("");
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    list()
      .then((res) => {
        if (alive) setRows(res.rows as Row[]);
      })
      .catch((e) => alive && setErr(e instanceof Error ? e.message : "Failed to load"));
    return () => {
      alive = false;
    };
  }, [list]);

  const filtered = useMemo(() => {
    if (!rows) return [];
    const needle = q.trim().toLowerCase();
    return rows.filter((r) => {
      if (filter !== "all" && r.user_type !== filter) return false;
      if (!needle) return true;
      return (
        r.name.toLowerCase().includes(needle) ||
        r.email.toLowerCase().includes(needle) ||
        r.phone.toLowerCase().includes(needle) ||
        (r.city ?? "").toLowerCase().includes(needle)
      );
    });
  }, [rows, q, filter]);

  const exportXlsx = () => {
    if (!rows || rows.length === 0) {
      toast.error("Nothing to export");
      return;
    }
    const flat = filtered.map((r) => ({
      ID: r.id,
      "Submitted at": new Date(r.created_at).toLocaleString(),
      Type: r.user_type,
      Name: r.name,
      Phone: r.phone,
      Email: r.email,
      City: r.city ?? "",
      Status: r.status,
      ...Object.fromEntries(
        Object.entries(r.answers ?? {}).map(([k, v]) => [`Q: ${k}`, v]),
      ),
    }));
    const ws = XLSX.utils.json_to_sheet(flat);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Responses");
    XLSX.writeFile(wb, `rentshield-responses-${new Date().toISOString().slice(0, 10)}.xlsx`);
  };

  return (
    <main className="mx-auto max-w-6xl px-5 py-8">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Responses</h1>
          <p className="text-sm text-muted-foreground">
            Signed in as {email} · {rows?.length ?? 0} total
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={exportXlsx}
            className="inline-flex h-10 items-center gap-2 rounded-full bg-foreground px-4 text-sm font-semibold text-background transition hover:opacity-90"
          >
            <Download className="h-4 w-4" /> Export Excel
          </button>
          <button
            onClick={() => supabase.auth.signOut()}
            className="inline-flex h-10 items-center gap-2 rounded-full border border-border bg-background px-4 text-sm font-medium text-foreground transition hover:bg-secondary"
          >
            <LogOut className="h-4 w-4" /> Sign out
          </button>
        </div>
      </div>

      <div className="mt-6 flex flex-wrap items-center gap-3">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Search name, email, phone, city"
            className="h-10 w-72 rounded-full border border-border bg-background pl-9 pr-3 text-sm outline-none transition focus:border-accent focus:ring-2 focus:ring-accent/20"
          />
        </div>
        <div className="flex gap-1 rounded-full border border-border bg-background p-1">
          {(["all", "renter", "owner"] as const).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`rounded-full px-3 py-1.5 text-xs font-medium capitalize transition ${
                filter === f
                  ? "bg-foreground text-background"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      {err && (
        <div className="mt-6 rounded-xl border border-destructive/40 bg-destructive/5 p-4 text-sm text-destructive">
          {err}
        </div>
      )}

      {!rows && !err && (
        <div className="mt-12 flex justify-center">
          <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
        </div>
      )}

      {rows && (
        <div className="mt-6 overflow-hidden rounded-2xl border border-border bg-card">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border bg-secondary/50 text-left text-xs uppercase tracking-wider text-muted-foreground">
                  <th className="px-4 py-3 font-medium">Date</th>
                  <th className="px-4 py-3 font-medium">Type</th>
                  <th className="px-4 py-3 font-medium">Name</th>
                  <th className="px-4 py-3 font-medium">Contact</th>
                  <th className="px-4 py-3 font-medium">City</th>
                  <th className="px-4 py-3 font-medium">Highlights</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((r) => (
                  <tr key={r.id} className="border-b border-border last:border-0 align-top">
                    <td className="whitespace-nowrap px-4 py-3 text-muted-foreground">
                      {new Date(r.created_at).toLocaleString()}
                    </td>
                    <td className="px-4 py-3">
                      <span
                        className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${
                          r.user_type === "renter"
                            ? "bg-accent/10 text-accent"
                            : "bg-success/10 text-success"
                        }`}
                      >
                        {r.user_type}
                      </span>
                    </td>
                    <td className="px-4 py-3 font-medium">{r.name}</td>
                    <td className="px-4 py-3">
                      <div>{r.email}</div>
                      <div className="text-muted-foreground">{r.phone}</div>
                    </td>
                    <td className="px-4 py-3">{r.city ?? "—"}</td>
                    <td className="px-4 py-3 text-xs text-muted-foreground">
                      <div className="max-w-md space-y-0.5">
                        {Object.entries(r.answers ?? {})
                          .slice(0, 4)
                          .map(([k, v]) => (
                            <div key={k}>
                              <span className="font-medium text-foreground">{k}:</span> {v}
                            </div>
                          ))}
                      </div>
                    </td>
                  </tr>
                ))}
                {filtered.length === 0 && (
                  <tr>
                    <td colSpan={6} className="px-4 py-12 text-center text-muted-foreground">
                      No responses match.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </main>
  );
}

function AuthInput({
  label,
  type,
  value,
  onChange,
  placeholder,
  required,
}: {
  label: string;
  type: string;
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
  required?: boolean;
}) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-sm font-medium text-foreground">{label}</span>
      <input
        type={type}
        value={value}
        required={required}
        placeholder={placeholder}
        onChange={(e) => onChange(e.target.value)}
        className="block w-full rounded-xl border border-input bg-background px-4 py-3 text-base outline-none transition focus:border-accent focus:ring-2 focus:ring-accent/20"
      />
    </label>
  );
}
