from flask import Flask, request, render_template, jsonify, abort
# from my_tweepy import upload_media_from_urls_and_get_ids  # Importing the function

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, world'


@app.route('/api/gettweetmediaids', methods=['POST'])
def gettweetmediaids():
    # Log the entire request JSON for debugging
    print("Incoming request JSON:", request.json)
    
    # Ensure the request is in JSON format
    if not request.is_json:
        return jsonify({'error': 'Request must be in JSON format'}), 400
    
    try:
        # Extract media_urls and log it for debugging
        media_urls = request.json.get('media_urls', None)
        print("Extracted media_urls:", media_urls)
        
        # If media_urls is a single string, convert it to a list
        if isinstance(media_urls, str):
            media_urls = [media_urls]
        
        # If media_urls is not a list or it's empty, return an error
        if not media_urls or not isinstance(media_urls, list):
            return jsonify({'error': 'Invalid or missing "media_urls"'}), 400
        
        # Example media ID response; replace with actual logic for media handling
        media_ids = ['1782411974233497600', '1782412005946642432']  # Dummy IDs for demonstration
        
        # Return the media IDs as JSON
        return jsonify({'media_ids': media_ids}), 200
    
    except KeyError:
        # Handle missing key error
        return jsonify({'error': 'Required key missing in request'}), 400
    
    except Exception as e:
        # Log the unexpected exception for further analysis
        print("Unexpected error in gettweetmediaids:", str(e))
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/gettweetmediaids', methods=['GET', 'PUT', 'DELETE'])
def method_not_allowed():
    return jsonify({'error': 'Only POST requests are supported on this endpoint'}), 405

@app.route('/test')
def test():
    return 'Test'

@app.route('/result')
def result():
   scores = {'phy': 50, 'che': 60, 'maths': 70}
   return render_template('result.html', result=scores)



@app.route('/api/extractwallet', methods=['POST'])
def extractwallet():
    # Log the entire request JSON for debugging
    print("Incoming request JSON:", request.json)
    
    # Ensure the request is in JSON format
    if not request.is_json:
        return jsonify({'error': 'Request must be in JSON format'}), 400
    
    try:
        # Extract media_urls and log it for debugging
        media_urls = request.json.get('media_urls', None)
        print("Extracted media_urls:", media_urls)
        
        # If media_urls is a single string, convert it to a list
        if isinstance(media_urls, str):
            media_urls = [media_urls]
        
        # If media_urls is not a list or it's empty, return an error
        if not media_urls or not isinstance(media_urls, list):
            return jsonify({'error': 'Invalid or missing "media_urls"'}), 400
        
        # Example media ID response; replace with actual logic for media handling
        media_ids = ['1782411974233497600', '1782412005946642432']  # Dummy IDs for demonstration
        
        # Return the media IDs as JSON
        return jsonify({'media_ids': media_ids}), 200
    
    except KeyError:
        # Handle missing key error
        return jsonify({'error': 'Required key missing in request'}), 400
    
    except Exception as e:
        # Log the unexpected exception for further analysis
        print("Unexpected error in gettweetmediaids:", str(e))
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/extractwallet', methods=['GET', 'PUT', 'DELETE'])
def method_not_allowed():
    return jsonify({'error': 'Only POST requests are supported on this endpoint'}), 405