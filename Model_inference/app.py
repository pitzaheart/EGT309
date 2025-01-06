from flask import Flask, request, jsonify, render_template, send_from_directory
import pandas as pd
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Add route for the main page
@app.route('/')
def home():
    return render_template('k8sUI.html')

@app.route('/forecast', methods=['POST'])
def generate_forecast():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Save the file temporarily
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Read the CSV file
            df = pd.read_csv(filepath)
            
            # Here you would call your forecasting model
            # For now, we'll return dummy results
            result = {
                'average_price': 500000,
                'min_price': 450000,
                'max_price': 550000,
                'confidence_score': 95
            }
            
            # Clean up - remove the temporary file
            os.remove(filepath)
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)