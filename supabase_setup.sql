-- Supabase Leaderboard Table Setup
-- Run this SQL in your Supabase SQL Editor

-- Create the leaderboard table
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

-- Create an index on total_score for faster sorting
CREATE INDEX IF NOT EXISTS idx_leaderboard_total_score ON leaderboard(total_score DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE leaderboard ENABLE ROW LEVEL SECURITY;

-- Create a policy that allows anyone to read the leaderboard
CREATE POLICY "Anyone can read leaderboard" ON leaderboard
    FOR SELECT
    USING (true);

-- Create a policy that allows anyone to insert into the leaderboard
-- (You may want to restrict this in production)
CREATE POLICY "Anyone can insert into leaderboard" ON leaderboard
    FOR INSERT
    WITH CHECK (true);

-- Optional: Create a policy to allow updates (if needed)
-- CREATE POLICY "Anyone can update leaderboard" ON leaderboard
--     FOR UPDATE
--     USING (true);

-- Optional: Create a policy to allow deletes (if needed)
-- CREATE POLICY "Anyone can delete from leaderboard" ON leaderboard
--     FOR DELETE
--     USING (true);
