from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle
app = Flask(__name__)
loaded_model = pickle.load(open('Finalmodel.pkl', 'rb'))
loaded_preprocessor = pickle.load(open('preprocessor.pkl', 'rb'))
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/submit', methods=['POST'])
def submit():
    Pregnancies = int(request.form['Pregnancies'])
    Glucose = int(request.form['Glucose'])
    BloodPressure = int(request.form['BloodPressure'])
    SkinThickness = int(request.form['SkinThickness'])
    Insulin = int(request.form['Insulin'])
    BMI = float(request.form['BMI'])
    DiabetesPedigreeFunction = float(request.form['DiabetesPedigreeFunction'])
    Age = int(request.form['Age']) 
    data = {
        'Pregnancies': [Pregnancies],
        'Glucose': [Glucose],
        'BloodPressure': [BloodPressure],
        'SkinThickness': [SkinThickness],
        'Insulin': [Insulin],
        'BMI': [BMI],
        'DiabetesPedigreeFunction': [DiabetesPedigreeFunction],
        'Age': [Age],
    }
    data_df = pd.DataFrame(data)
    processed_data = loaded_preprocessor.transform(data_df)
    pred = loaded_model.predict(processed_data)
    def check_disease(pred):
        if pred == 0:
            return "Healthy!!! :-)"
        elif pred == 1:
            return "Diabetes confirmed!! :-("
    pred_ = check_disease(pred)
    return render_template('blog.html', predict=pred_)
if __name__ == '__main__':
    app.run(debug=True)
