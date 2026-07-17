from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import requests
import hashlib
import json
from datetime import datetime, timedelta
import random
import time
import os
from breach_news import BREACH_NEWS
from csv_checker import check_email_in_csv, get_csv_stats, get_random_breach

app = Flask(__name__)
app.config['SECRET_KEY'] = 'winning-hackathon-2024'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# ==================== MASSIVE BREACH DATABASE ====================
BREACH_DATABASE = {
    "test@example.com": [
        {
            "Name": "LinkedIn 2021 Mega Breach",
            "BreachDate": "2021-06-22",
            "Description": "700 MILLION LinkedIn user records found on dark web.",
            "DataClasses": ["Email Addresses", "Phone Numbers", "Work History"],
            "AccountsAffected": "700,000,000",
            "Severity": "CRITICAL",
            "DarkWebSources": ["RaidsForum", "BreachForums"],
            "Status": "Active"
        },
        {
            "Name": "Adobe Creative Cloud Leak",
            "BreachDate": "2023-10-04",
            "Description": "153 MILLION Adobe accounts compromised.",
            "DataClasses": ["Email Addresses", "Encrypted Passwords"],
            "AccountsAffected": "153,000,000",
            "Severity": "CRITICAL",
            "DarkWebSources": ["DarkMarket"],
            "Status": "Active"
        }
    ],
    "admin@gmail.com": [
        {
            "Name": "Canva Design Platform Breach",
            "BreachDate": "2024-05-24",
            "Description": "139 MILLION Canva accounts exposed.",
            "DataClasses": ["Email Addresses", "Names", "Password Hashes"],
            "AccountsAffected": "139,000,000",
            "Severity": "HIGH",
            "DarkWebSources": ["RaidForums"],
            "Status": "Active"
        }
    ]
}

# ==================== DARK WEB MARKET DATA ====================
DARK_WEB_MARKETS = [
    {"name": "🇷🇺 Russian Market", "listings": "12,847", "status": "🔥 ACTIVE", "type": "Credentials"},
    {"name": "🌐 BreachForums", "listings": "25,601", "status": "🟢 ONLINE", "type": "Forum"},
    {"name": "💀 Exploit.in", "listings": "15.2M", "status": "🔥 ACTIVE", "type": "Database"},
]

# ==================== LIVE THREAT FEED ====================
LIVE_THREATS = [
    {"type": "critical", "message": "🚨 2.5M credentials dropped on RaidsForum", "time": "2 mins ago", "source": "RaidsForum"},
    {"type": "critical", "message": "💀 Russian Market selling 1.2M VPN logins", "time": "5 mins ago", "source": "Russian Market"},
    {"type": "warning", "message": "⚠️ New ransomware 'DarkVault' targeting healthcare", "time": "12 mins ago", "source": "DarkWeb Intel"},
]

# ==================== ROUTES ====================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_breach():
    try:
        data = request.get_json()
        email = data.get('email', '').lower().strip()
        
        if not email:
            return jsonify({'error': 'Email required'}), 400
        
        # Get CSV stats
        csv_stats = get_csv_stats()
        
        # Check in CSV first (this adds 8-12 second delay automatically)
        found_in_csv, csv_row, csv_message = check_email_in_csv(email)
        
        # Check in database
        if email in BREACH_DATABASE:
            breaches = BREACH_DATABASE[email]
            risk_score = 100 if any(b['Severity'] == 'CRITICAL' for b in breaches) else 75
            
            response = {
                'success': True,
                'email': email,
                'breaches': breaches,
                'total_breaches': len(breaches),
                'risk_score': risk_score,
                'csv_checked': True,
                'csv_message': csv_message,
                'csv_stats': csv_stats,
                'remediation': generate_remediation(risk_score),
                'timestamp': datetime.now().isoformat()
            }
            return jsonify(response)
        
        # If found in CSV but not in database
        if found_in_csv and csv_row:
            csv_breach = {
                "Name": csv_row.get('breach_source', 'Data Breach'),
                "BreachDate": f"{csv_row.get('breach_year', '2021')}-01-01",
                "Description": f"Your email found in {csv_row.get('breach_source', 'dataset')}",
                "DataClasses": csv_row.get('data_found', 'email').split(','),
                "AccountsAffected": csv_stats['rows'],
                "Severity": "MEDIUM",
                "DarkWebSources": ["Dark Web Dataset"],
                "Status": "Active"
            }
            
            return jsonify({
                'success': True,
                'email': email,
                'breaches': [csv_breach],
                'total_breaches': 1,
                'risk_score': 65,
                'csv_checked': True,
                'csv_message': csv_message,
                'csv_stats': csv_stats,
                'remediation': generate_remediation(65),
                'timestamp': datetime.now().isoformat()
            })
        
        # Not found anywhere - 70% chance of random breach for demo
        if random.random() < 0.7:
            companies = [
                {"Name": "LinkedIn", "Severity": "CRITICAL", "AccountsAffected": "700M"},
                {"Name": "Facebook", "Severity": "CRITICAL", "AccountsAffected": "533M"},
            ]
            company = random.choice(companies)
            year = random.randint(2020, 2024)
            
            breach = [{
                "Name": f"{company['Name']} Data Breach",
                "BreachDate": f"{year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                "Description": f"{company['AccountsAffected']} {company['Name']} user records found on dark web.",
                "DataClasses": ["Email Addresses", "Passwords"],
                "AccountsAffected": company['AccountsAffected'],
                "Severity": company['Severity'],
                "Status": "Active"
            }]
            
            return jsonify({
                'success': True,
                'email': email,
                'breaches': breach,
                'total_breaches': 1,
                'risk_score': 75,
                'csv_checked': True,
                'csv_message': csv_message,
                'csv_stats': csv_stats,
                'remediation': generate_remediation(75),
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': True,
                'email': email,
                'breaches': [],
                'total_breaches': 0,
                'risk_score': 15,
                'csv_checked': True,
                'csv_message': csv_message,
                'csv_stats': csv_stats,
                'remediation': ['✅ No breaches found', '🔐 Enable 2FA for security'],
                'timestamp': datetime.now().isoformat()
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_remediation(risk_score):
    steps = [
        '🔐 Change passwords immediately',
        '📱 Enable Two-Factor Authentication',
        '🔄 Use a password manager',
    ]
    if risk_score > 80:
        steps.insert(0, '⚠️ URGENT: Your data is on dark web!')
    return steps

# ==================== API ENDPOINTS ====================
@app.route('/api/breach-news')
def get_breach_news():
    return jsonify(BREACH_NEWS)

@app.route('/api/stats')
def get_stats():
    csv_stats = get_csv_stats()
    return jsonify({
        'total_breaches': format(random.randint(15000, 20000), ','),
        'records_exposed': f"{random.randint(10, 15)}B",
        'active_threats': random.randint(400, 600),
        'scans_today': format(random.randint(50000, 80000), ','),
        'dataset_records': csv_stats['rows']
    })

@app.route('/api/live-threats')
def get_live_threats():
    threats = LIVE_THREATS.copy()
    random.shuffle(threats)
    return jsonify(threats[:5])

@app.route('/api/markets')
def get_markets():
    return jsonify(DARK_WEB_MARKETS)

@app.route('/api/csv-info')
def csv_info():
    return jsonify(get_csv_stats())

@app.route('/health')
def health():
    csv_stats = get_csv_stats()
    return jsonify({
        'status': 'operational',
        'csv_loaded': csv_stats['rows'] > 0,
        'records': csv_stats['rows']
    })

# ==================== MAIN ====================
if __name__ == '__main__':
    csv_stats = get_csv_stats()
    print("\n" + "="*60)
    print("🚀 DARK WEB BREACH MONITOR - BACKUP PLAN")
    print("="*60)
    print(f"✅ CSV Dataset: {csv_stats['rows']} records")
    print(f"✅ Breach News: {len(BREACH_NEWS)} articles")
    print(f"✅ Preset Breaches: {len(BREACH_DATABASE)}")
    print("="*60)
    print("📍 URL: http://localhost:5000")
    print("="*60 + "\n")
    
    socketio.run(app, debug=True, port=5000)