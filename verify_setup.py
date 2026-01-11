#!/usr/bin/env python3
"""
Quick verification script to check Supabase setup
Run this to verify your database is ready before deploying
"""

import requests

def check_supabase_setup():
    """Check if Supabase project and table are set up correctly"""

    # These should match your .streamlit/secrets.toml
    SUPABASE_URL = "https://sfnxksgdpiusivswyjow.supabase.co"
    SUPABASE_KEY = "sb_secret_V03Jbsm49XdcxLr9CrO7EA_hoXwOifI"  # Replace with your anon key

    print("🔍 Verifying Supabase setup...\n")

    # Test 1: Check if Supabase project is accessible
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/", headers={"apikey": SUPABASE_KEY}, timeout=10)
        if response.status_code in [200, 401, 403]:  # 401/403 is OK if RLS is enabled
            print("✅ Supabase project is accessible")
        else:
            print(f"❌ Supabase project returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to Supabase: {e}")
        return False

    # Test 2: Check if leaderboard table exists
    try:
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }

        # Try to select from leaderboard table
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/leaderboard?select=count",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            try:
                data = response.json()
                count = len(data) if isinstance(data, list) else 0
                print(f"✅ Leaderboard table exists - contains {count} records")
            except:
                print("✅ Leaderboard table exists")
        elif response.status_code == 404:
            print("❌ Leaderboard table does not exist")
            print("💡 SOLUTION: Run supabase_setup.sql in Supabase SQL Editor")
            return False
        elif response.status_code in [401, 403]:
            print("❌ Permission denied - check RLS policies or use correct key")
            print("💡 SOLUTION: Make sure you're using the anon key, not service_role")
            return False
        else:
            print(f"❌ Unexpected response: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error testing table access: {e}")
        return False

    # Test 3: Try to insert a test record
    try:
        test_data = {
            "player": "TestUser",
            "total_score": 1000,
            "songs_played": 1,
            "avg_score": 1000,
            "genre": "Test",
            "date": "Jan 01"
        }

        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/leaderboard",
            headers=headers,
            json=test_data,
            timeout=10
        )

        if response.status_code in [200, 201]:
            print("✅ Can insert records into leaderboard table")

            # Clean up test record
            try:
                # Get the test record we just inserted
                response = requests.get(
                    f"{SUPABASE_URL}/rest/v1/leaderboard?player=eq.TestUser",
                    headers=headers,
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    if data and len(data) > 0:
                        record_id = data[0]['id']
                        # Delete the test record
                        requests.delete(
                            f"{SUPABASE_URL}/rest/v1/leaderboard?id=eq.{record_id}",
                            headers=headers,
                            timeout=10
                        )
                        print("✅ Test record cleaned up")
            except:
                pass  # Ignore cleanup errors

        elif response.status_code in [401, 403]:
            print("❌ Cannot insert records - permission denied")
            print("💡 SOLUTION: Check RLS policies in Supabase dashboard")
            return False
        else:
            print(f"❌ Cannot insert records: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error testing insert: {e}")
        return False

    print("\n🎉 Supabase setup is complete and working!")
    print("✅ Project accessible")
    print("✅ Leaderboard table exists")
    print("✅ Can read and write data")
    return True

if __name__ == "__main__":
    success = check_supabase_setup()
    if not success:
        print("\n❌ Setup verification failed")
        print("Follow the setup instructions in SUPABASE_SETUP.md")
    else:
        print("\n🚀 Your app should work correctly now!")