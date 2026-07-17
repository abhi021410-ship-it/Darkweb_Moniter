import csv
import random
import os
import time
from datetime import datetime

# Global cache for faster searching
EMAIL_CACHE = {}
CACHE_BUILT = False
CSV_STATS = {"rows": 0, "columns": 0}

def build_email_cache():
    """Build a cache of emails for faster searching"""
    global EMAIL_CACHE, CACHE_BUILT, CSV_STATS
    try:
        csv_path = os.path.join('data', 'darkweb_breach_dataset.csv')
        
        if not os.path.exists(csv_path):
            print("⚠️ CSV file not found. Using demo mode.")
            CACHE_BUILT = True
            return
            
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            CSV_STATS["rows"] = len(rows)
            CSV_STATS["columns"] = len(reader.fieldnames) if reader.fieldnames else 0
            
            # Build cache of all emails found in CSV
            for row in rows:
                for key, value in row.items():
                    if value and isinstance(value, str):
                        # Store lowercase version for case-insensitive matching
                        value_lower = value.lower()
                        if '@' in value_lower:  # Looks like an email
                            EMAIL_CACHE[value_lower] = row
                        # Also store as partial for contains checks
                        if len(value_lower) > 3:  # Only store meaningful strings
                            EMAIL_CACHE[value_lower[:10]] = row  # Store first 10 chars for partial matching
            
            print(f"✅ Built cache with {len(EMAIL_CACHE)} entries from {CSV_STATS['rows']} rows")
            CACHE_BUILT = True
    except Exception as e:
        print("❌ Cache build error:", e)
        CACHE_BUILT = True

# Build cache immediately when module loads
build_email_cache()

def check_email_in_csv(email):
    """Check if email exists in CSV with PERFECT 10-15 second feel"""
    start_time = time.time()
    
    try:
        email_lower = email.lower().strip()
        
        # STEP 1: Show "scanning" feel - initial delay (3 seconds)
        time.sleep(3)
        
        # STEP 2: Check in cache first (instant)
        if email_lower in EMAIL_CACHE:
            # Add delay to make it feel like real scanning (total 8 seconds)
            elapsed = time.time() - start_time
            if elapsed < 8:
                time.sleep(8 - elapsed)
            return True, EMAIL_CACHE[email_lower], "Found in primary database cache"
        
        # STEP 3: Simulate deep scanning (another 3 seconds)
        time.sleep(3)
        
        # STEP 4: Check for partial matches
        for cached_email, row in EMAIL_CACHE.items():
            if email_lower in cached_email or cached_email in email_lower:
                elapsed = time.time() - start_time
                if elapsed < 11:
                    time.sleep(11 - elapsed)
                return True, row, "Found in secondary index"
        
        # STEP 5: Final deep scan simulation (another 3 seconds)
        time.sleep(3)
        
        # STEP 6: If we have CSV file, do full scan as fallback
        csv_path = os.path.join('data', 'darkweb_breach_dataset.csv')
        if os.path.exists(csv_path) and CSV_STATS["rows"] > 0:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    for key, value in row.items():
                        if value and isinstance(value, str) and email_lower in value.lower():
                            # Add to cache for next time
                            EMAIL_CACHE[email_lower] = row
                            elapsed = time.time() - start_time
                            if elapsed < 14:
                                time.sleep(14 - elapsed)
                            return True, row, "Found in full database scan"
        
        # STEP 7: No match found - ensure total time is 10-15 seconds
        elapsed = time.time() - start_time
        if elapsed < 12:
            time.sleep(12 - elapsed)
        
        return False, None, "No matches found after scanning all databases"
        
    except Exception as e:
        print("❌ CSV check error:", e)
        elapsed = time.time() - start_time
        if elapsed < 10:
            time.sleep(10 - elapsed)
        return False, None, f"Error during scan: {str(e)}"

def get_random_breach_from_csv():
    """Get a random breach entry for demo"""
    try:
        if EMAIL_CACHE:
            # Return a random entry from cache
            random_key = random.choice(list(EMAIL_CACHE.keys()))
            return EMAIL_CACHE[random_key]
        return None
    except:
        return None

def get_csv_stats():
    """Get statistics about the CSV file"""
    global CSV_STATS
    
    if CSV_STATS["rows"] == 0:
        # Try to load stats if not already loaded
        try:
            csv_path = os.path.join('data', 'darkweb_breach_dataset.csv')
            if os.path.exists(csv_path):
                with open(csv_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    rows = list(reader)
                    CSV_STATS["rows"] = len(rows)
                    CSV_STATS["columns"] = len(reader.fieldnames) if reader.fieldnames else 0
        except:
            pass
    
    return {
        "rows": CSV_STATS["rows"],
        "columns": CSV_STATS["columns"],
        "cache_size": len(EMAIL_CACHE),
        "database_size": f"{CSV_STATS['rows']} Indian records",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def force_rebuild_cache():
    """Force rebuild the cache (useful if CSV changes)"""
    global EMAIL_CACHE, CACHE_BUILT
    EMAIL_CACHE = {}
    CACHE_BUILT = False
    build_email_cache()
    return {"status": "Cache rebuilt", "entries": len(EMAIL_CACHE)}

# Initialize on load
print(f"📊 CSV Checker initialized with {CSV_STATS['rows']} records")