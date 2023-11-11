# app.py
from flask import Flask, render_template, request, jsonify
import fasttext
import re
from flask_cors import CORS
from flask_mysqldb import MySQL
from db_config import DATABASE_CONFIG  # assuming you have a separate file for database configuration

app = Flask(__name__)
CORS(app)
model = fasttext.load_model("C:\Payment_Type_Classifiation\model.bin")

app.config['MYSQL_HOST'] = DATABASE_CONFIG['host']
app.config['MYSQL_USER'] = DATABASE_CONFIG['user']
app.config['MYSQL_PASSWORD'] = DATABASE_CONFIG['password']
app.config['MYSQL_DB'] = DATABASE_CONFIG['db']
app.config['MYSQL_SSL_CA'] = DATABASE_CONFIG['ssl_ca']

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        data = request.get_json().get('data')  # Extract data from JSON in the request body
        amount = request.get_json().get('amount')
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

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO payment_history (Prediction, Amount) VALUES (%s, %s)", (result, amount))
            mysql.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()

        return jsonify({'prediction': result, 'amount': amount})  # Return prediction as JSON

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
