from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import cv2
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Define a home route for basic testing
@app.route("/")
def home():
    return "Welcome to the Image Background Remover API!"

# Endpoint to process and remove background
@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files["image"]
    image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Perform background removal with GrabCut
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    bgd_model = np.zeros((1, 65), dtype=np.float64)
    fgd_model = np.zeros((1, 65), dtype=np.float64)
    rect = (10, 10, image.shape[1] - 30, image.shape[0] - 30)
    cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

    # Refine the mask for the foreground
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")

    # Create a white background
    result_with_white_bg = np.ones_like(image, dtype=np.uint8) * 255  # white background
    result_with_white_bg[mask2 == 1] = image[mask2 == 1]  # Apply the foreground only where mask is 1

    # Save the processed image
    output_path = "output.png"
    cv2.imwrite(output_path, result_with_white_bg)

    # Return the image to the frontend
    return send_from_directory(directory=os.getcwd(), path=output_path)

if __name__ == "__main__":
    app.run(debug=True)
