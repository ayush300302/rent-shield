
-- Lock down user_roles: no client should be able to write. Only service_role (server) manages roles.
REVOKE INSERT, UPDATE, DELETE ON public.user_roles FROM anon, authenticated, PUBLIC;

-- Submissions go through the server function (supabaseAdmin / service_role), so drop public insert on responses.
DROP POLICY IF EXISTS "Anyone can insert responses" ON public.responses;
REVOKE INSERT ON public.responses FROM anon, authenticated, PUBLIC;

-- has_role must remain executable for authenticated users because RLS policies on
-- public.responses invoke it as the calling role. Revoke from anon/public to minimize exposure.
REVOKE EXECUTE ON FUNCTION public.has_role(uuid, app_role) FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION public.has_role(uuid, app_role) TO authenticated, service_role;
