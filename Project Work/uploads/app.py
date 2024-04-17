import os
from flask import Flask, request, render_template
from PIL import Image
import numpy as np
import tensorflow as tf

app = Flask(__name__, template_folder='templates')
model = tf.keras.models.load_model('Final_model_tmt.h5')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/gallery')
def gallery():
    return render_template('gallery-single.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/predict')
def pred():
    return render_template('predict.html')

@app.route('/result', methods=['POST'])
def predict():
    if request.method == "POST":
        f = request.files['file']
        if f.filename == '':
            return render_template('results.html', prediction_text="No file selected")
        
        # Save and process the image
        basepath = os.path.dirname(__file__)
        filepath = os.path.join(basepath, 'uploads', f.filename)
        f.save(filepath)
        image = Image.open(filepath)
        image = image.resize((256, 256))  # Resize image to match model input size
        image = np.asarray(image) / 255.0  # Normalize image
        image = np.expand_dims(image, axis=0)  # Add batch dimension
        
        # Make prediction
        prediction = model.predict(image)
        class_index = np.argmax(prediction)
        
        # Map class index to class name
        class_names = ['Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___healthy',
                       'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
                       'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot',
                       'Tomato___Tomato_mosaic_virus', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus']
        predicted_class = class_names[class_index]
        
        # Prepare message based on predicted class
        if predicted_class == 'Tomato___healthy':
            prediction_text = "Provided Tomato Plant Leaf is Healthy :)"
        else:
            prediction_text = f"The tomato plant leaf is having:\n{predicted_class.replace('Tomato___', '')} :(" 
        
        return render_template('results.html', prediction_text=prediction_text)


if __name__ == "__main__":
    app.run(debug=True)