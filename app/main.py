import os
import sys

# Ensure the parent directory is in the path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from app.storyboard import create_storyboard_stream

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    text = data.get('text', '')
    style = data.get('style', 'Realistic')
    
    if not text or not text.strip():
        return jsonify({"error": "No text provided"}), 400
        
    def stream_generator():
        try:
            for chunk in create_storyboard_stream(text, style):
                yield chunk
        except Exception as e:
            # Yield error in JSON lines format as a fallback mechanism 
            import json
            yield json.dumps({"error": str(e)}) + "\n"
            
    return Response(stream_with_context(stream_generator()), mimetype='application/jsonl')

if __name__ == '__main__':
    # Ensure static directories exist
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'static', 'generated_images'), exist_ok=True)
    app.run(debug=True, port=5000)
