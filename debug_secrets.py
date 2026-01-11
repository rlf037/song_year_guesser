#!/usr/bin/env python3
"""
Debug script to test Supabase secrets access and database connection
Run this locally to verify everything is working before deploying
"""

import streamlit as st

def test_supabase_secrets():
    """Test function to debug Supabase secrets access"""
    print("=== SUPABASE SECRETS TEST ===")

    try:
        # Print all available secrets (safely)
        if hasattr(st.secrets, 'keys'):
            keys = list(st.secrets.keys())
            print(f"📋 Available secrets keys: {keys}")
        else:
            print("⚠️ st.secrets has no keys method")
            return False

        # Test supabase section
        if "supabase" in st.secrets:
            print("✅ Found 'supabase' section")
            try:
                url = st.secrets.supabase.SUPABASE_URL
                key = st.secrets.supabase.SUPABASE_KEY
                print(f"✅ Attribute access worked")
                print(f"   URL: {url[:30]}..." if url else "   URL: None")
                print(f"   KEY: {key[:15]}..." if key else "   KEY: None")

                if key and key.startswith("sb_secret_"):
                    print("⚠️  WARNING: Using service_role key - should use anon key")

                return True, url, key
            except AttributeError as e:
                print(f"❌ Attribute access failed: {e}")
                try:
                    url = st.secrets["supabase"]["SUPABASE_URL"]
                    key = st.secrets["supabase"]["SUPABASE_KEY"]
                    print(f"✅ Dict access worked")
                    print(f"   URL: {url[:30]}..." if url else "   URL: None")
                    print(f"   KEY: {key[:15]}..." if key else "   KEY: None")
                    return True, url, key
                except (KeyError, TypeError) as e2:
                    print(f"❌ Dict access failed: {e2}")
        else:
            print("❌ No 'supabase' section found")

        # Test top-level keys
        url = st.secrets.get("SUPABASE_URL", "")
        key = st.secrets.get("SUPABASE_KEY", "")
        if url and key:
            print(f"✅ Top-level keys worked")
            print(f"   URL: {url[:30]}..." if url else "   URL: None")
            print(f"   KEY: {key[:15]}..." if key else "   KEY: None")
            return True, url, key
        else:
            print(f"❌ Top-level keys failed: URL={bool(url)}, KEY={bool(key)}")

        return False, None, None
    except Exception as e:
        print(f"❌ ERROR in secrets test: {e}")
        import traceback
        traceback.print_exc()
        return False, None, None

def test_database_connection(url, key):
    """Test actual database connection"""
    print("\n=== DATABASE CONNECTION TEST ===")

    try:
        from supabase import create_client
        print("🔧 Creating Supabase client...")
        client = create_client(url, key)
        print("✅ Client created")

        print("🔍 Testing connection...")
        # Try to count records in leaderboard table
        response = client.table("leaderboard").select("count", count="exact").execute()
        print("✅ Connection successful - leaderboard table exists")

        # Try to get some data
        data_response = client.table("leaderboard").select("*").limit(5).execute()
        if data_response.data:
            print(f"✅ Found {len(data_response.data)} records in table")
            for i, record in enumerate(data_response.data[:3]):
                print(f"   Record {i+1}: {record.get('player', 'Unknown')} - {record.get('total_score', 0)} pts")
        else:
            print("ℹ️  Table exists but is empty")

        return True

    except Exception as e:
        error_str = str(e).lower()
        print(f"❌ Database connection failed: {e}")

        if "relation" in error_str or "does not exist" in error_str:
            print("💡 SOLUTION: Run supabase_setup.sql in Supabase SQL Editor")
        elif "permission" in error_str or "policy" in error_str or "unauthorized" in error_str:
            print("💡 SOLUTION: Check RLS policies or use correct key type")
        elif "invalid" in error_str:
            print("💡 SOLUTION: Use anon public key, not service_role key")

        return False

if __name__ == "__main__":
    print("🧪 Testing Supabase setup...\n")

    success, url, key = test_supabase_secrets()

    if success and url and key:
        print("\n✅ Secrets accessible!")
        db_success = test_database_connection(url, key)
        if db_success:
            print("\n🎉 Everything is working!")
        else:
            print("\n❌ Database connection failed - check setup")
    else:
        print("\n❌ Secrets not accessible")
        print("\n💡 Check your .streamlit/secrets.toml file:")
        print("   [supabase]")
        print("   SUPABASE_URL = \"your_project_url\"")
        print("   SUPABASE_KEY = \"your_anon_key\"")