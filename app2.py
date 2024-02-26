# app.py
from flask import Flask, render_template, request, jsonify
import fasttext
import json
import re
from datetime import datetime
from decimal import Decimal
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
    return render_template('home.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/analysis.html')
def analysis():
    return render_template('analysis.html')
    


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        data = request.get_json().get('data')  # Extract data from JSON in the request body
        amount = request.get_json().get('amount')
        print(data)
        from transformers import pipeline
        zero_shot_classifier = pipeline("zero-shot-classification")
        result = zero_shot_classifier(sequences=data,
                              candidate_labels=['Transportation', 'Rent & Utilities', 'Travel', 'Medical', 'Loans',
                                                'General Services',
                                                'General Merchandise', 'Food & Drink', 'Entertainment',
                                                'Bank Transfers'], multi_class=True)
        max_score_label, max_score = max(zip(result["labels"], result["scores"]), key=lambda x: x[1])

        print(f"{max_score_label}: {max_score}")

        result= max_score_label

        try:
            cursor = mysql.connection.cursor()
            date = datetime.now()
            print(date)

            cursor.execute("INSERT INTO payment_history (Prediction, Amount, Date) VALUES (%s, %s, %s)", (result, amount,date))
            mysql.connection.commit()
            print("Success")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            

        return jsonify({'prediction': result, 'amount': amount})  # Return prediction as JSON
    

@app.route('/analysis_pred', methods=['POST'])


    
def analysis_pred():
    if request.method == 'POST':
        data = request.get_json()  # Extract JSON data from the request body
        print("inside /analysis_pred")

        # Extract start and end dates from the JSON data
        print(data)
        start_date = data.get('startDate')
        end_date = data.get('endDate')
        print(start_date)
        print(end_date)
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        start_date = start_date.date()
        end_date = end_date.date()
        print(start_date)
        print(end_date)

        # SQL query to sum amounts for each prediction between the given start and end dates
        sql_query = """
            SELECT Prediction, SUM(Amount) as TotalAmount
            FROM payment_history
            WHERE Date BETWEEN %s AND %s
            GROUP BY Prediction;
        """
        print("Query framed")
        try:
            cursor = mysql.connection.cursor()

            # Execute the query with the start and end dates as parameters
            cursor.execute(sql_query, (start_date, end_date))


            # Fetch the result
            result = cursor.fetchall()
            print(result)
            # result = {'category': [], 'amount': []}
            data_list = [{'category': item[0], 'amount': float(item[1])} for item in result]
            print(data_list)
            json_data = json.dumps(data_list)
            return json_data
        

        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify({'error': 'An error occurred during analysis'})

        finally:
            if 'cursor' in locals():
                cursor.close()

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
