-- =====================================================================
-- Supabase Schema for PM Internship Scheme Recommender Engine (Bulletproof SQL)
-- Target Table: public.internships
-- Project Ref: otcbofqdjxaegqekyjmn
-- =====================================================================

-- 1. Create the internships table
CREATE TABLE IF NOT EXISTS public.internships (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    internship_id VARCHAR(100) UNIQUE NOT NULL,
    company_name TEXT NOT NULL,
    title TEXT NOT NULL,
    sector TEXT NOT NULL,
    required_skills TEXT NOT NULL,
    required_education TEXT NOT NULL,
    location TEXT NOT NULL,
    stipend INTEGER DEFAULT 0,
    apply_link TEXT DEFAULT '#',
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 2. Add performance indexes for common search filters
CREATE INDEX IF NOT EXISTS idx_internships_sector ON public.internships (sector);
CREATE INDEX IF NOT EXISTS idx_internships_location ON public.internships (location);
CREATE INDEX IF NOT EXISTS idx_internships_internship_id ON public.internships (internship_id);

-- 3. Enable Row Level Security (RLS)
ALTER TABLE public.internships ENABLE ROW LEVEL SECURITY;

-- 4. Recreate RLS Policies safely
DROP POLICY IF EXISTS "Allow public read access" ON public.internships;
DROP POLICY IF EXISTS "Allow public insert and update" ON public.internships;

CREATE POLICY "Allow public read access"
    ON public.internships
    FOR SELECT
    USING (true);

CREATE POLICY "Allow public insert and update"
    ON public.internships
    FOR ALL
    USING (true)
    WITH CHECK (true);
