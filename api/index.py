from flask import Flask, request, render_template, jsonify, abort, redirect

app = Flask(__name__)

# Define redirection rules based on path
def get_redirect_url(path):
    if path == '/path1':
        return 'https://intermediary-url1.vercel.app/'
    elif path == '/path2':
        return 'https://intermediary-url2.vercel.app/'
    # Add more cases for additional paths and intermediary URLs as needed
    else:
        return 'https://default-intermediary-url.vercel.app/'

# Route to handle redirection based on the requested path
@app.route('/')
def redirect_path():
    path = request.path
    redirect_url = get_redirect_url(path)
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
