from flask import Flask, render_template, request


import fasttext

app = Flask(__name__)
model = fasttext.load_model("C:\Payment_Type_Classifiation\model.bin")  # Double backslashes in the path

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        data = request.form.get('data')  
        print(data)
        result = model.predict(data)
        return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
