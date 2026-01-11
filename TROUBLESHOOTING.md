# Troubleshooting Guide

## Database Connection Issues

### Problem: "Database not configured" error

**Symptoms:**
- When saving scores, you get "Database not configured" or "Secrets check: URL=True, KEY=True"
- Scores are saved locally but not to the database

**Solutions:**

1. **Check Streamlit Cloud Secrets**
   ```
   [supabase]
   SUPABASE_URL = "https://sfnxksgdpiusivswyjow.supabase.co"
   SUPABASE_KEY = "your_anon_key_here"
   ```

2. **Get the correct Supabase keys:**
   - Go to Supabase Dashboard → Settings → API
   - Copy the **Project URL** (not the REST URL)
   - Copy the **anon public** key (NOT service_role)

3. **Update secrets in Streamlit Cloud:**
   - Go to your Streamlit Cloud app → Settings → Secrets
   - Paste the correct secrets format
   - The app will redeploy automatically

### Problem: "Table 'leaderboard' doesn't exist"

**Solution:**
1. Go to Supabase Dashboard → SQL Editor
2. Create a new query
3. Copy and paste the contents of `supabase_setup.sql`
4. Click "Run"

### Problem: "Permission denied" or RLS errors

**Solutions:**
1. **Check RLS policies** in Supabase Dashboard → Table Editor → leaderboard → Policies
2. Make sure you have:
   - SELECT policy allowing all users
   - INSERT policy allowing all users
3. **Use the correct key type** - anon key, not service_role

### Problem: Service role key instead of anon key

**Symptoms:**
- Key starts with `sb_secret_`
- In-app debug shows: "⚠️ Using service_role key - should use anon public key"
- Database client creation fails

**Solution:**
1. Go to Supabase Dashboard → Settings → API
2. Copy the **anon public** key (NOT service_role)
3. Update Streamlit Cloud secrets:
   ```toml
   [supabase]
   SUPABASE_URL = "https://your-project.supabase.co"
   SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # anon key
   ```
4. The anon key is safe for client applications and what Streamlit apps should use

## Testing Your Setup

### 1. Local Testing
```bash
# Test secrets access
streamlit run debug_secrets.py

# Test full database connection
python verify_setup.py
```

### 2. In-App Testing
- Open your Streamlit app
- Look for the "🔧 Debug & Diagnostics" section
- Click "🧪 Test Database Connection"
- Check the results

### 3. Streamlit Cloud Logs
- Go to Streamlit Cloud → Manage app → Logs
- Look for detailed error messages starting with DEBUG, ERROR, etc.

## Common Issues and Fixes

| Error Message | Likely Cause | Solution |
|---------------|--------------|----------|
| "Database not configured" | Secrets not set in Streamlit Cloud | Update secrets in Streamlit Cloud dashboard |
| "Table doesn't exist" | SQL setup not run | Run `supabase_setup.sql` in SQL Editor |
| "Permission denied" | RLS policies missing | Check/create policies in Supabase |
| "Invalid key" | Wrong key type used | Use anon key, not service_role |
| "Connection failed" | Network/firewall issues | Check Supabase status or try different network |

## Quick Setup Checklist

- [ ] Supabase project created
- [ ] `supabase_setup.sql` run in SQL Editor
- [ ] Correct secrets in Streamlit Cloud:
  ```toml
  [supabase]
  SUPABASE_URL = "https://your-project.supabase.co"
  SUPABASE_KEY = "your-anon-key"
  ```
- [ ] Anon key used (not service_role)
- [ ] RLS policies created
- [ ] App redeployed after secrets update

## Getting Help

If you're still having issues:

1. **Check the debug output** in Streamlit Cloud logs
2. **Run the verification scripts** locally
3. **Use the in-app debug tool** in the welcome screen
4. **Verify your Supabase dashboard** - make sure the project exists and is active

The debug output will tell you exactly what's wrong and how to fix it.