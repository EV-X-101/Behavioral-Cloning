import cv2
import numpy as np
from keras.models import load_model

class_names = {
    0: 'Speed limit (20km/h)',
    1: 'Speed limit (30km/h)',
    2: 'Speed limit (50km/h)',
    3: 'Speed limit (60km/h)',
    4: 'Speed limit (70km/h)',
    5: 'Speed limit (80km/h)',
    6: 'End of speed limit (80km/h)',
    7: 'Speed limit (100km/h)',
    8: 'Speed limit (120km/h)',
    9: 'No passing',
    10: 'No passing for vehicles over 3.5 metric tons',
    11: 'Right-of-way at the next intersection',
    12: 'Priority road',
    13: 'Yield',
    14: 'Stop',
    15: 'No vehicles',
    16: 'Vehicles over 3.5 metric tons prohibited',
    17: 'No entry',
    18: 'General caution',
    19: 'Dangerous curve to the left',
    20: 'Dangerous curve to the right',
    21: 'Double curve',
    22: 'Bumpy road',
    23: 'Slippery road',
    24: 'Road narrows on the right',
    25: 'Road work',
    26: 'Traffic signals',
    27: 'Pedestrians',
    28: 'Children crossing',
    29: 'Bicycles crossing',
    30: 'Beware of ice/snow',
    31: 'Wild animals crossing',
    32: 'End of all speed and passing limits',
    33: 'Turn right ahead',
    34: 'Turn left ahead',
    35: 'Ahead only',
    36: 'Go straight or right',
    37: 'Go straight or left',
    38: 'Keep right',
    39: 'Keep left',
    40: 'Roundabout mandatory',
    41: 'End of no passing',
    42: 'End of no passing by vehicles over 3.5 metric tons'
}

def preprocess(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.equalizeHist(img)
    img = cv2.resize(img, (32, 32))
    img = img / 255
    return img

def predict_sign(img_path, model_path):
    # Load the trained model
    model = load_model(model_path)

    # Read the image file
    img = cv2.imread(img_path)

    # Make sure that img is not None
    if img is not None:
        # Preprocess the image
        img_preprocessed = preprocess(img)
        img_preprocessed = img_preprocessed.reshape(1, 32, 32, 1)

        # Generate the model's predictions
        predictions = model.predict(img_preprocessed)

        # Get the index of the class with the highest probability
        predicted_class = np.argmax(predictions)

        # Look up the name of the predicted sign based on its class index
        predicted_name = class_names[predicted_class]

        # Convert the processed image to color format for displaying the text on it
        processed_img_gray = (img_preprocessed.squeeze() * 255).astype(np.uint8)
        processed_img_color = cv2.cvtColor(processed_img_gray, cv2.COLOR_GRAY2BGR)

        # Display the predicted name on the image
        font_scale = 1
        thickness = 2

        # Determine the font scale based on the image size
        height, width, _ = processed_img_color.shape
        font_scale = min(height, width) / 500

        font = cv2.FONT_HERSHEY_SIMPLEX
        bottom_left_corner_of_text = (10, int(30 * font_scale))
        font_color = (0, 255, 0)
        line_type = cv2.LINE_AA

        cv2.putText(processed_img_color, predicted_name, 
                    bottom_left_corner_of_text, 
                    font, 
                    font_scale,
                    font_color,
                    thickness,
                    line_type)

        # Resize the image to a larger size for display
        resized_img = cv2.resize(processed_img_color, (500, 500))

        # Return the predicted name and the image
        return predicted_name, resized_img

    else:
        # Return an error message if the image could not be loaded
        return "Error: Failed to load image at {img_path}", None