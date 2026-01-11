# Supabase Setup Guide

## Quick Setup (3 Steps)

### Step 1: Create the Database Table

1. Go to your Supabase project: https://supabase.com/dashboard/project/sfnxksgdpiusivswyjow
2. Navigate to **SQL Editor** in the left sidebar
3. Click **New Query**
4. Copy and paste the contents of `supabase_setup.sql`
5. Click **Run** (or press Cmd/Ctrl + Enter) to execute the SQL

This will create the `leaderboard` table with the correct schema and permissions.

### Step 2: Get Your Supabase Keys

1. In your Supabase project, go to **Settings** (gear icon) → **API**
2. Copy the **Project URL** → This is your `SUPABASE_URL`
   - Should be: `https://sfnxksgdpiusivswyjow.supabase.co`
3. Copy the **anon public** key → This is your `SUPABASE_KEY`
   - Look for the key labeled "anon" or "public" (NOT "service_role")

**Important:** Use the `anon` key for security. The service_role key has full access and should not be used in client applications.

### Step 3: Configure Streamlit Cloud Secrets

**This is the critical step!** Your local secrets file won't work on Streamlit Cloud.

1. Go to your Streamlit Cloud dashboard: https://share.streamlit.io/
2. Find and select your app: **song-year-game** (or whatever it's named)
3. Click the **⋮** (three dots) menu → **Settings** → **Secrets**
4. Paste the following into the secrets editor:

```toml
[spotify]
client_id = "cdd8156aa4ed49f8a5bff380a38d5cf3"
client_secret = "6b0eb8be224a48c180127e5efbef28a3"

SUPABASE_URL = "https://sfnxksgdpiusivswyjow.supabase.co"
SUPABASE_KEY = "YOUR_ANON_KEY_HERE"
```

5. Replace `YOUR_ANON_KEY_HERE` with the anon key from Step 2
6. Click **Save**
7. Your app will automatically redeploy

## Step 3: Verify the Setup

After configuring:
1. Restart your Streamlit app
2. Play a game and click "End Game"
3. You should see "✅ Score saved to database!" instead of the warning message
4. Check your Supabase table to see the entry

## Troubleshooting

### "Database not configured" message:
- Check that secrets are set in Streamlit Cloud (not just locally)
- Verify the SUPABASE_URL and SUPABASE_KEY are correct
- Make sure you're using the `anon` key, not `service_role`

### "Permission denied" error:
- Check that Row Level Security (RLS) policies are set up correctly
- Verify the policies in Supabase allow INSERT operations

### Table doesn't exist:
- Run the SQL script in Supabase SQL Editor
- Check that the table name is exactly `leaderboard` (lowercase)
