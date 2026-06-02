
-- Roles enum + table
CREATE TYPE public.app_role AS ENUM ('admin', 'user');

CREATE TABLE public.user_roles (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  role app_role NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (user_id, role)
);

GRANT SELECT ON public.user_roles TO authenticated;
GRANT ALL ON public.user_roles TO service_role;
ALTER TABLE public.user_roles ENABLE ROW LEVEL SECURITY;

CREATE OR REPLACE FUNCTION public.has_role(_user_id uuid, _role app_role)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public
AS $$
  SELECT EXISTS (
    SELECT 1 FROM public.user_roles WHERE user_id = _user_id AND role = _role
  )
$$;

CREATE POLICY "Users can view own roles" ON public.user_roles
  FOR SELECT TO authenticated USING (auth.uid() = user_id);

-- Responses table
CREATE TABLE public.responses (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at timestamptz NOT NULL DEFAULT now(),
  user_type text NOT NULL CHECK (user_type IN ('renter','owner')),
  answers jsonb NOT NULL DEFAULT '{}'::jsonb,
  name text NOT NULL,
  phone text NOT NULL,
  email text NOT NULL,
  city text,
  source text,
  utm jsonb,
  status text NOT NULL DEFAULT 'new',
  notes text
);

CREATE INDEX idx_responses_created_at ON public.responses (created_at DESC);
CREATE INDEX idx_responses_user_type ON public.responses (user_type);

GRANT INSERT ON public.responses TO anon, authenticated;
GRANT SELECT ON public.responses TO authenticated;
GRANT ALL ON public.responses TO service_role;
ALTER TABLE public.responses ENABLE ROW LEVEL SECURITY;

-- Anyone (including anonymous) can submit
CREATE POLICY "Anyone can insert responses" ON public.responses
  FOR INSERT TO anon, authenticated WITH CHECK (true);

-- Only admins can read
CREATE POLICY "Admins can view all responses" ON public.responses
  FOR SELECT TO authenticated USING (public.has_role(auth.uid(), 'admin'));

CREATE POLICY "Admins can update responses" ON public.responses
  FOR UPDATE TO authenticated USING (public.has_role(auth.uid(), 'admin'));
