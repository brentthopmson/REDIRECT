from flask import Flask, request, render_template, jsonify, abort
# from my_tweepy import upload_media_from_urls_and_get_ids  # Importing the function

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, world'
    return jsonify({'error': 'Only POST requests are supported on this endpoint'}), 405

@app.route('/test')
def test():
    return 'Test'

@app.route('/result')
def result():
   scores = {'phy': 50, 'che': 60, 'maths': 70}
   return render_template('result.html', result=scores)

