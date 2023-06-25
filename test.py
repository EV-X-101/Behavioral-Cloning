from predict_sign import predict_sign
import cv2

img_path = 'TS Data/IMG/stop.jpg'
model_path = 'Models/TSmodel.h5'

# Call the predict_sign function
predicted_name, processed_img = predict_sign(img_path, model_path)

# Check if an error occurred
if "Error" in predicted_name:
    print(predicted_name)
else:
    # Display the predicted name and image
    print(f"Predicted sign name: {predicted_name}")
    cv2.imshow('image', processed_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()