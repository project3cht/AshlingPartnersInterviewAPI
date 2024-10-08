from flask import Flask, jsonify, request
from marshmallow import Schema, fields, ValidationError
import logging
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.exceptions import NotFittedError
# from mtcnn import MTCNN
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
# import io
# import base64

# Initialize Flask app
app = Flask(__name__)

# Set the logger level for Flask's logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize a simple Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Initialize MTCNN model
#detection = MTCNN()

# Sample data for training the model (replace with your actual data)
X_train = np.random.rand(100, 4)
y_train = np.random.randint(0, 2, 100)
model.fit(X_train, y_train)

#validate input schema
class FeaturesSchema(Schema):
    features = fields.List(fields.Float(), required=True, validate=lambda x: len(x) == 4)

@app.route('/')
def hello():
    logger.info('Main endpoint processing HTTP request')
    return jsonify({"success":True, "message": "Hello, World!"})


@app.route('/predict', methods=['POST'])
def predict():
    logger.info('Prediction endpoint processing HTTP request')
    
    # Input validation
    schema = FeaturesSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        logger.error(f'Invalid input: {err.messages}')
        return jsonify({"success": False, "error": err.messages}), 400
    
    features = request.json['features']
    
    try:
        # Make prediction
        prediction = model.predict([features])[0]
        logger.info(f'Prediction made: {prediction}')
        return jsonify({"success": True, "prediction": int(prediction)}), 200
    except NotFittedError:
        logger.error('Model not fitted')
        return jsonify({"success": False, "error": "Model not fitted"}), 500
    except Exception as e:
        logger.error(f'Error during prediction: {str(e)}')
        return jsonify({"success": False, "error": "Error during prediction"}), 500
    
#My perosnal laptop does not have enough ram to load cxomputer vision models as well as docker at the same time.
#If alloted more time I would like to research deploying an api with cloud computers in order to offload the computational load.

# @app.route('/detect_face', methods=['POST'])
# def detect_face():
#     app.logger.info('Face detction endpoint processing HTTP request')

#     #Check if image is in request
#     if 'image' not in request.files:
#         app.logger.info('No Image file in the response')
#         return jsonify({"succes": False, "error": "No Image file in the request"}),400
    
#     #Fetch and Read in image
#     image_file = request.files['image']
#     image = Image.open(image_file)
#     image_np = np.array(image)

#     #Find Faces
#     faces = detection.detect_faces(image_np)

#     if not faces:
#         app.logger.info('No Faces Detected in the image')
#         return jsonify({"success": True, "message": "No faces Detected in the image"})
    
#     # Save image to buffer
#     buffer = io.BytesIO()
#     image.save(buffer, format="PNG")
#     buffer.seek(0)

#     #Encode image to base64
#     img_str = base64.b64encode(buffer.getvalue().decode())

#     #return the image with number of faces
#     app.logger.info(f'Detected {len(faces)} face(s) in the image')
#     return jsonify({
#         "success": True, 
#         "num_faces": len(faces),
#         "image": img_str
#     })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=50505)