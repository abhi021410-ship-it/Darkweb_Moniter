import csv
import os
import time
import random
from datetime import datetime

# Global variables
CSV_DATA = []
CSV_STATS = {"rows": 0, "columns": 0, "loaded": False}
EMAIL_CACHE = {}

def load_csv_data():
    """Load CSV data into memory"""
    global CSV_DATA, CSV_STATS, EMAIL_CACHE
    
    csv_path = os.path.join('data', 'sample_breach_data.csv')
    
    try:
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                CSV_DATA = list(reader)
                CSV_STATS["rows"] = len(CSV_DATA)
                CSV_STATS["columns"] = len(reader.fieldnames) if reader.fieldnames else 0
                
                # Build email cache for faster lookup
                for row in CSV_DATA:
                    if 'email' in row and row['email']:
                        EMAIL_CACHE[row['email'].lower().strip()] = row
                
                CSV_STATS["loaded"] = True
                print(f"✅ CSV loaded: {CSV_STATS['rows']} records")
        else:
            print("⚠️ CSV file not found, using empty dataset")
            CSV_DATA = []
            CSV_STATS["rows"] = 0
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        CSV_DATA = []
        CSV_STATS["rows"] = 0

# Load CSV when module starts
load_csv_data()

def check_email_in_csv(email):
    """
    Check if email exists in CSV with 5-10 second delay
    Returns: (found, row_data, message)
    """
    start_time = time.time()
    email_lower = email.lower().strip()
    
    # STEP 1: Initial scanning message (2 seconds)
    time.sleep(2)
    
    # STEP 2: Check in cache (instant)
    if email_lower in EMAIL_CACHE:
        # Add remaining delay to make it 8-12 seconds total
        elapsed = time.time() - start_time
        target_time = random.uniform(8, 12)
        if elapsed < target_time:
            time.sleep(target_time - elapsed)
        
        return True, EMAIL_CACHE[email_lower], f"✅ Email found in breach dataset ({CSV_STATS['rows']} records scanned)"
    
    # STEP 3: Simulate full scan (3 seconds)
    time.sleep(3)
    
    # STEP 4: Check all rows (fast but feels like scanning)
    for row in CSV_DATA:
        if 'email' in row and row['email'] and email_lower == row['email'].lower().strip():
            # Add to cache for next time
            EMAIL_CACHE[email_lower] = row
            
            # Ensure total time is 8-12 seconds
            elapsed = time.time() - start_time
            target_time = random.uniform(8, 12)
            if elapsed < target_time:
                time.sleep(target_time - elapsed)
            
            return True, row, f"✅ Email found in breach dataset ({CSV_STATS['rows']} records scanned)"
    
    # STEP 5: No match found - still wait to look real
    elapsed = time.time() - start_time
    target_time = random.uniform(8, 12)
    if elapsed < target_time:
        time.sleep(target_time - elapsed)
    
    return False, None, f"✅ No match found in dataset ({CSV_STATS['rows']} records scanned)"

def get_csv_stats():
    """Get statistics about the CSV file"""
    global CSV_STATS
    
    # Try to load if not loaded
    if not CSV_STATS["loaded"]:
        load_csv_data()
    
    return {
        "rows": CSV_STATS["rows"],
        "columns": CSV_STATS["columns"],
        "loaded": CSV_STATS["loaded"],
        "cache_size": len(EMAIL_CACHE),
        "message": f"Dataset contains {CSV_STATS['rows']} breach records"
    }

def get_random_breach():
    """Get a random breach from CSV for demo purposes"""
    if CSV_DATA:
        return random.choice(CSV_DATA)
    return None

# Initialize on load
print(f"📊 CSV Checker ready with {CSV_STATS['rows']} records")