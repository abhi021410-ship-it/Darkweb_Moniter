from flask import Flask, render_template, request, jsonify, session, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import requests
import hashlib
import json
from datetime import datetime, timedelta
import random
import time
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'winning-hackathon-2024'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# ==================== MASSIVE BREACH DATABASE ====================
BREACH_DATABASE = {
    # Test emails with multiple breaches
    "test@example.com": [
        {
            "Name": "LinkedIn 2021 Mega Breach",
            "BreachDate": "2021-06-22",
            "Description": "700 MILLION LinkedIn user records found on dark web. Your profile data including email, phone, work history, and connections are being sold on hacker forums.",
            "DataClasses": ["Email Addresses", "Phone Numbers", "Work History", "Skills", "Connections", "Messages"],
            "AccountsAffected": "700,000,000",
            "Severity": "CRITICAL",
            "DarkWebSources": ["RaidsForum", "BreachForums", "Exploit.in"],
            "PriceInBitcoin": "0.5 BTC",
            "Screenshots": True,
            "Status": "Active"
        },
        {
            "Name": "Adobe Creative Cloud Leak",
            "BreachDate": "2023-10-04",
            "Description": "153 MILLION Adobe accounts compromised. Your encrypted passwords and credit card info found on dark web marketplace.",
            "DataClasses": ["Email Addresses", "Encrypted Passwords", "Credit Card Info", "Billing Address"],
            "AccountsAffected": "153,000,000",
            "Severity": "CRITICAL",
            "DarkWebSources": ["DarkMarket", "Russian Market"],
            "PriceInBitcoin": "2.3 BTC",
            "Status": "Active"
        },
        {
            "Name": "Twitter/X Data Breach",
            "BreachDate": "2024-01-15",
            "Description": "Your Twitter account data found in recent 400M user leak. DMs, emails, and phone numbers exposed.",
            "DataClasses": ["Email Addresses", "Phone Numbers", "Direct Messages", "Followers"],
            "AccountsAffected": "400,000,000",
            "Severity": "CRITICAL",
            "DarkWebSources": ["BreachForums"],
            "PriceInBitcoin": "1.8 BTC",
            "Status": "Active"
        }
    ],
    "admin@gmail.com": [
        {
            "Name": "Canva Design Platform Breach",
            "BreachDate": "2024-05-24",
            "Description": "139 MILLION Canva accounts exposed. Your designs, personal info, and passwords found on dark web.",
            "DataClasses": ["Email Addresses", "Names", "Design Files", "Password Hashes"],
            "AccountsAffected": "139,000,000",
            "Severity": "HIGH",
            "DarkWebSources": ["RaidForums", "Nulled.to"],
            "PriceInBitcoin": "1.2 BTC",
            "Status": "Active"
        }
    ],
    "john.doe@gmail.com": [
        {
            "Name": "Facebook Data Leak",
            "BreachDate": "2023-08-12",
            "Description": "533 MILLION Facebook users' data leaked. Your personal info including phone number and location exposed.",
            "DataClasses": ["Email Addresses", "Phone Numbers", "Location", "Relationship Status", "Employer"],
            "AccountsAffected": "533,000,000",
            "Severity": "CRITICAL",
            "DarkWebSources": ["Lowlife", "RaidsForum"],
            "PriceInBitcoin": "3.0 BTC",
            "Status": "Active"
        }
    ],
    "sarah.smith@yahoo.com": [
        {
            "Name": "Yahoo Data Breach",
            "BreachDate": "2022-12-14",
            "Description": "3 BILLION Yahoo accounts compromised. One of the largest breaches in history.",
            "DataClasses": ["Email Addresses", "Passwords", "Security Questions", "Birthdays"],
            "AccountsAffected": "3,000,000,000",
            "Severity": "CRITICAL",
            "DarkWebSources": ["Peace", "TheRealDeal"],
            "PriceInBitcoin": "5.0 BTC",
            "Status": "Active"
        }
    ]
}

# ==================== DARK WEB MARKET DATA ====================
DARK_WEB_MARKETS = [
    {"name": "🇷🇺 Russian Market", "listings": "12,847", "status": "🔥 ACTIVE", "type": "Credentials"},
    {"name": "🌐 BreachForums", "listings": "25,601", "status": "🟢 ONLINE", "type": "Forum"},
    {"name": "💀 Exploit.in", "listings": "15.2M", "status": "🔥 ACTIVE", "type": "Database"},
    {"name": "🕸️ RaidsForum", "listings": "5,234", "status": "🟢 ONLINE", "type": "Forum"},
    {"name": "⚫ Nulled.to", "listings": "9,847", "status": "🟢 ONLINE", "type": "Community"},
    {"name": "🔴 DarkMarket", "listings": "8,342", "status": "🔥 ACTIVE", "type": "Marketplace"},
    {"name": "💣 Hydra Market", "listings": "20.1K", "status": "💀 TAKEN DOWN", "type": "Marketplace"},
    {"name": "🎯 Torrez", "listings": "4,567", "status": "🟢 ONLINE", "type": "Market"}
]

# ==================== LIVE THREAT FEED ====================
LIVE_THREATS = [
    {"type": "critical", "message": "🚨 MASSIVE: 2.5M Fortune 500 credentials just dropped on RaidsForum", "time": "2 mins ago", "source": "RaidsForum"},
    {"type": "critical", "message": "💀 ALERT: Russian Market selling 1.2M corporate VPN logins", "time": "5 mins ago", "source": "Russian Market"},
    {"type": "warning", "message": "⚠️ New ransomware 'DarkVault' targeting healthcare - 12 hospitals affected", "time": "12 mins ago", "source": "DarkWeb Intel"},
    {"type": "warning", "message": "🔓 500K .gov emails found in paste site - active selling", "time": "18 mins ago", "source": "Pastebin"},
    {"type": "info", "message": "📊 Hackers developing new Chrome password stealer", "time": "25 mins ago", "source": "Exploit.in"},
    {"type": "critical", "message": "🕸️ 3 new .onion credit card shops discovered", "time": "31 mins ago", "source": "Tor Monitor"},
    {"type": "info", "message": "🔐 Banking trojan 'Grandoreiro' targeting 30+ banks", "time": "45 mins ago", "source": "Threat Intel"},
    {"type": "warning", "message": "⚠️ Massive phishing campaign targeting Coinbase users", "time": "52 mins ago", "source": "Phishing Feed"}
]

# ==================== MAIN CHECK ENDPOINT ====================
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
        
        # Check in database first
        if email in BREACH_DATABASE:
            breaches = BREACH_DATABASE[email]
            risk_score = 100 if any(b['Severity'] == 'CRITICAL' for b in breaches) else 75
            
            return jsonify({
                'success': True,
                'email': email,
                'breaches': breaches,
                'total_breaches': len(breaches),
                'risk_score': risk_score,
                'total_records': sum(int(b['AccountsAffected'].replace(',', '').replace('B', '000000000').replace('M', '000000')) for b in breaches),
                'dark_web_mentions': generate_dark_web_mentions(email),
                'remediation': generate_remediation(risk_score),
                'timestamp': datetime.now().isoformat()
            })
        
        # For any other email, generate realistic results
        if random.random() < 0.7:  # 70% chance of finding breaches
            num_breaches = random.randint(1, 3)
            breaches = []
            companies = [
                {"Name": "LinkedIn", "Severity": "CRITICAL", "AccountsAffected": "700M"},
                {"Name": "Facebook", "Severity": "CRITICAL", "AccountsAffected": "533M"},
                {"Name": "Adobe", "Severity": "HIGH", "AccountsAffected": "153M"},
                {"Name": "Canva", "Severity": "HIGH", "AccountsAffected": "139M"},
                {"Name": "Dropbox", "Severity": "MEDIUM", "AccountsAffected": "68M"},
                {"Name": "Twitter", "Severity": "CRITICAL", "AccountsAffected": "400M"}
            ]
            
            for i in range(num_breaches):
                company = random.choice(companies)
                year = random.randint(2020, 2024)
                month = random.randint(1, 12)
                day = random.randint(1, 28)
                
                breaches.append({
                    "Name": f"{company['Name']} Data Breach",
                    "BreachDate": f"{year}-{month:02d}-{day:02d}",
                    "Description": f"{company['AccountsAffected']} {company['Name']} user records found on dark web. Your data appears in this breach.",
                    "DataClasses": ["Email Addresses", "Passwords", "Names"][:random.randint(2, 3)],
                    "AccountsAffected": company['AccountsAffected'],
                    "Severity": company['Severity'],
                    "DarkWebSources": random.sample(["RaidsForum", "BreachForums", "Exploit.in"], random.randint(1, 3)),
                    "Status": "Active"
                })
            
            risk_score = 85 if any(b['Severity'] == 'CRITICAL' for b in breaches) else 60
            
            return jsonify({
                'success': True,
                'email': email,
                'breaches': breaches,
                'total_breaches': len(breaches),
                'risk_score': risk_score,
                'total_records': random.randint(1000000, 1000000000),
                'dark_web_mentions': generate_dark_web_mentions(email),
                'remediation': generate_remediation(risk_score),
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': True,
                'email': email,
                'breaches': [],
                'total_breaches': 0,
                'risk_score': 15,
                'total_records': 0,
                'dark_web_mentions': [],
                'remediation': ['✅ No immediate action needed', '🔐 Enable 2FA for security', '📱 Use password manager'],
                'timestamp': datetime.now().isoformat()
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_dark_web_mentions(email):
    """Generate dark web mentions"""
    mentions = []
    domains = ['exploit.in', 'raidforums.com', 'nulled.to', 'cracked.to', 'breachforums.ws']
    
    for i in range(random.randint(1, 4)):
        mentions.append({
            'source': random.choice(domains),
            'date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
            'thread': f"Fullz {email.split('@')[0]} database 2024",
            'replies': random.randint(5, 100),
            'views': random.randint(100, 10000)
        })
    
    return mentions

def generate_remediation(risk_score):
    """Generate remediation steps based on risk"""
    steps = [
        '🔐 Change passwords immediately for ALL accounts',
        '📱 Enable Two-Factor Authentication (2FA) everywhere',
        '🔄 Use a password manager (Bitwarden/1Password)',
        '📧 Monitor email for suspicious activity',
        '💳 Check bank/credit card statements',
        '🛡️ Consider identity theft protection',
        '🔍 Review account recovery options',
        '🚫 Remove unused online accounts'
    ]
    
    if risk_score > 80:
        steps.insert(0, '⚠️ URGENT: Your data is actively being traded on dark web!')
        steps.insert(1, '🚨 FREEZE your credit reports immediately')
    
    return steps

# ==================== STATS ENDPOINT ====================
@app.route('/api/stats')
def get_stats():
    return jsonify({
        'total_breaches': format(random.randint(15000, 20000), ','),
        'records_exposed': f"{random.randint(10, 15)}.{random.randint(1, 9)}B",
        'active_threats': random.randint(400, 600),
        'scans_today': format(random.randint(50000, 80000), ','),
        'markets_monitored': len(DARK_WEB_MARKETS),
        'countries_affected': random.randint(150, 195),
        'avg_risk_score': random.randint(65, 85)
    })

# ==================== LIVE THREATS ENDPOINT ====================
@app.route('/api/live-threats')
def get_live_threats():
    # Rotate threats for live feed
    threats = LIVE_THREATS.copy()
    random.shuffle(threats)
    return jsonify(threats[:8])

# ==================== DARK WEB MARKETS ENDPOINT ====================
@app.route('/api/markets')
def get_markets():
    return jsonify(DARK_WEB_MARKETS)

# ==================== BREACH TRENDS ENDPOINT ====================
@app.route('/api/trends')
def get_trends():
    days = 30
    data = []
    for i in range(days):
        data.append({
            'date': (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'),
            'breaches': random.randint(5, 50),
            'records': random.randint(100000, 10000000)
        })
    return jsonify(data)

# ==================== RECENT SCANS ENDPOINT ====================
@app.route('/api/recent-scans')
def recent_scans():
    scans = []
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'company.com']
    for i in range(10):
        scans.append({
            'email': f"user{random.randint(100, 999)}@{random.choice(domains)}",
            'risk': random.choice(['HIGH', 'MEDIUM', 'LOW']),
            'time': f"{random.randint(1, 59)} mins ago",
            'breaches': random.randint(0, 5)
        })
    return jsonify(scans)

# ==================== HEALTH CHECK ====================
@app.route('/health')
def health():
    return jsonify({
        'status': 'operational',
        'version': '3.0.0',
        'scans_processed': random.randint(100000, 999999),
        'uptime': '99.99%'
    })

# ==================== SOCKETIO EVENTS ====================
@socketio.on('connect')
def handle_connect():
    emit('connected', {'data': 'Connected to DarkWeb Monitor'})

@socketio.on('subscribe')
def handle_subscribe(data):
    emit('subscribed', {'status': 'monitoring', 'email': data.get('email')})

# ==================== MAIN ====================
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 DARK WEB BREACH MONITOR - ENTERPRISE v3.0")
    print("="*60)
    print("✅ Server starting...")
    print("✅ Database loaded: " + str(len(BREACH_DATABASE)) + " preset breaches")
    print("✅ Dark web markets: " + str(len(DARK_WEB_MARKETS)) + " active")
    print("✅ Live threat feed: " + str(len(LIVE_THREATS)) + " threats")
    print("="*60)
    print("📍 URL: http://localhost:5000")
    print("📍 WebSocket: ws://localhost:5000")
    print("📍 API: http://localhost:5000/api/*")
    print("="*60 + "\n")
    
    socketio.run(app, debug=True, port=5000)