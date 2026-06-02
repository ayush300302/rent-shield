import { createServerFn } from "@tanstack/react-start";
import { z } from "zod";

const SubmitSchema = z.object({
  user_type: z.enum(["renter", "owner"]),
  answers: z.record(z.string().max(64), z.string().max(256)),
  name: z.string().trim().min(1).max(120),
  phone: z.string().trim().min(7).max(20).regex(/^[+\d\s\-()]+$/, "Invalid phone"),
  email: z.string().trim().email().max(200),
  source: z.string().max(120).optional().nullable(),
});

export const submitResponse = createServerFn({ method: "POST" })
  .inputValidator((input) => SubmitSchema.parse(input))
  .handler(async ({ data }) => {
    const { supabaseAdmin } = await import("@/integrations/supabase/client.server");
    const city =
      typeof data.answers.city === "string" ? data.answers.city : null;
    const { data: row, error } = await supabaseAdmin
      .from("responses")
      .insert({
        user_type: data.user_type,
        answers: data.answers,
        name: data.name,
        phone: data.phone,
        email: data.email,
        city,
        source: data.source ?? null,
      })
      .select("id")
      .single();
    if (error) throw new Error(error.message);
    return { id: row.id };
  });
