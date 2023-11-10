from flask import Flask, render_template, request, jsonify
import fasttext
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
model = fasttext.load_model("C:\Payment_Type_Classifiation\model.bin")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        data = request.get_json().get('data')  # Extract data from JSON in the request body
        print(data)
        
        result = model.predict(data)
        print(result)
        
        pattern = r"\(\('__label__(\w+)\'.*?\)"
        match = re.search(pattern, str(result))  # Convert result to string before applying regex
        
        if match:
            label = match.group(1)
            result = label
        else:
            print("No match found.")

        return jsonify({'prediction': result})  # Return prediction as JSON

if __name__ == '__main__':
    app.run(debug=True)
