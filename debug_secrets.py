#!/usr/bin/env python3
"""
Debug script to test Supabase secrets access
Run this locally to verify secrets are working before deploying
"""

import streamlit as st

def test_supabase_secrets():
    """Test function to debug Supabase secrets access"""
    print("=== SUPABASE SECRETS TEST ===")

    try:
        # Print all available secrets (safely)
        if hasattr(st.secrets, 'keys'):
            print(f"Available secrets keys: {list(st.secrets.keys())}")
        else:
            print("st.secrets has no keys attribute")

        # Test supabase section
        if "supabase" in st.secrets:
            print("✓ Found 'supabase' section")
            try:
                url = st.secrets.supabase.SUPABASE_URL
                key = st.secrets.supabase.SUPABASE_KEY
                print(f"✓ Attribute access worked: URL={bool(url)}, KEY={bool(key)}")
                print(f"  URL starts with: {url[:30] if url else 'None'}...")
                print(f"  KEY starts with: {key[:10] if key else 'None'}...")
                return True
            except AttributeError as e:
                print(f"✗ Attribute access failed: {e}")
                try:
                    url = st.secrets["supabase"]["SUPABASE_URL"]
                    key = st.secrets["supabase"]["SUPABASE_KEY"]
                    print(f"✓ Dict access worked: URL={bool(url)}, KEY={bool(key)}")
                    print(f"  URL starts with: {url[:30] if url else 'None'}...")
                    print(f"  KEY starts with: {key[:10] if key else 'None'}...")
                    return True
                except (KeyError, TypeError) as e2:
                    print(f"✗ Dict access failed: {e2}")
        else:
            print("✗ No 'supabase' section found")

        # Test top-level keys
        url = st.secrets.get("SUPABASE_URL", "")
        key = st.secrets.get("SUPABASE_KEY", "")
        if url and key:
            print(f"✓ Top-level keys worked: URL={bool(url)}, KEY={bool(key)}")
            print(f"  URL starts with: {url[:30] if url else 'None'}...")
            print(f"  KEY starts with: {key[:10] if key else 'None'}...")
            return True
        else:
            print(f"✗ Top-level keys failed: URL={bool(url)}, KEY={bool(key)}")

        return False
    except Exception as e:
        print(f"ERROR in secrets test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Supabase secrets access...")
    success = test_supabase_secrets()
    if success:
        print("\n✅ Secrets are accessible!")
    else:
        print("\n❌ Secrets are not accessible. Check your .streamlit/secrets.toml file.")

    # Try to create a client if secrets work
    if success:
        try:
            from supabase import create_client, Client
            print("\nTesting Supabase client creation...")
            # This would use the secrets, but we can't access them directly here
            print("Client creation would happen in the main app")
        except ImportError:
            print("❌ Supabase library not installed")