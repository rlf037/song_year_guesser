-- Supabase Leaderboard Table Setup
-- Run this SQL in your Supabase SQL Editor (Dashboard → SQL Editor → New Query)

-- Step 1: Create the leaderboard table
CREATE TABLE IF NOT EXISTS leaderboard (
    id BIGSERIAL PRIMARY KEY,
    player TEXT NOT NULL,
    total_score INTEGER NOT NULL,
    songs_played INTEGER NOT NULL,
    avg_score INTEGER NOT NULL,
    genre TEXT NOT NULL,
    date TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Step 2: Create an index on total_score for faster sorting
CREATE INDEX IF NOT EXISTS idx_leaderboard_total_score ON leaderboard(total_score DESC);

-- Step 3: Enable Row Level Security (RLS) - important for security
ALTER TABLE leaderboard ENABLE ROW LEVEL SECURITY;

-- Step 4: Create policies for reading and writing
-- Allow anyone to read the leaderboard (safe)
DROP POLICY IF EXISTS "Anyone can read leaderboard" ON leaderboard;
CREATE POLICY "Anyone can read leaderboard" ON leaderboard
    FOR SELECT
    USING (true);

-- Allow anyone to insert into the leaderboard (you may want to restrict this in production)
DROP POLICY IF EXISTS "Anyone can insert into leaderboard" ON leaderboard;
CREATE POLICY "Anyone can insert into leaderboard" ON leaderboard
    FOR INSERT
    WITH CHECK (true);

-- Optional: Allow updates and deletes (uncomment if needed)
-- DROP POLICY IF EXISTS "Anyone can update leaderboard" ON leaderboard;
-- CREATE POLICY "Anyone can update leaderboard" ON leaderboard
--     FOR UPDATE
--     USING (true);

-- DROP POLICY IF EXISTS "Anyone can delete from leaderboard" ON leaderboard;
-- CREATE POLICY "Anyone can delete from leaderboard" ON leaderboard
--     FOR DELETE
--     USING (true);

-- Verification: Check if table was created successfully
SELECT
    schemaname,
    tablename,
    tableowner
FROM pg_tables
WHERE tablename = 'leaderboard';

-- Verification: Check if RLS is enabled
SELECT
    schemaname,
    tablename,
    rowsecurity
FROM pg_tables
WHERE tablename = 'leaderboard';

-- Verification: Check policies
SELECT
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies
WHERE tablename = 'leaderboard';
