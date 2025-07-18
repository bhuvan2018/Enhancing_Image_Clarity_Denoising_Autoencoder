from flask import Flask, render_template, request, jsonify, send_file
from keras.layers import TFSMLayer
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import base64
import io
import os
import pandas as pd
from datetime import datetime
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
from sklearn.metrics import mean_absolute_error, mean_squared_error
import cv2

app = Flask(__name__)
model = TFSMLayer("autoencoder_model", call_endpoint="serving_default")
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def is_mobile_selfie(img_array):
    contrast = img_array.std()
    brightness = img_array.mean()
    return contrast < 0.08 and brightness > 0.3  # updated condition

def enhance_image_features(pil_img):
    # Convert to OpenCV format
    img_cv = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    # Mild Denoising
    img_cv = cv2.fastNlMeansDenoisingColored(img_cv, None, 5, 5, 5, 15)

    # Back to PIL
    pil_img = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))

    # Mild Contrast and Sharpness Enhancement
    pil_img = ImageEnhance.Contrast(pil_img).enhance(1.3)
    pil_img = ImageEnhance.Sharpness(pil_img).enhance(1.5)

    return pil_img

def subtle_enhancement(output_array):
    """
    Very subtle post-processing to just clean up the denoised output
    """
    # Ensure output is in valid range [0, 1]
    output_array = np.clip(output_array, 0, 1)
    
    # Convert to PIL for processing
    output_img = Image.fromarray((output_array * 255).astype('uint8'))
    
    # Very subtle sharpening - slightly increased for better detail
    output_img = output_img.filter(ImageFilter.UnsharpMask(radius=0.8, percent=60, threshold=1))
    
    # Minimal contrast adjustment
    enhancer = ImageEnhance.Contrast(output_img)
    output_img = enhancer.enhance(1.03)
    
    # Optional: Very slight brightness boost if image seems dark
    avg_brightness = np.mean(output_array)
    if avg_brightness < 0.4:  # Only brighten if image is quite dark
        enhancer = ImageEnhance.Brightness(output_img)
        output_img = enhancer.enhance(1.02)
    
    return output_img



def preprocess_image(image):
    image = image.convert('RGB')
    image = image.resize((128, 128))

    img_array = np.array(image).astype('float32') / 255.0

    if is_mobile_selfie(img_array):
        image = enhance_image_features(image)
        image = image.resize((128, 128))
        img_array = np.array(image).astype('float32') / 255.0

    if img_array.ndim == 2:
        img_array = np.stack((img_array,) * 3, axis=-1)
    elif img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]

    return np.expand_dims(img_array, axis=0)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/in')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    image_file = request.files['image']
    filename = image_file.filename
    image = Image.open(image_file).convert('RGB')
    processed = preprocess_image(image)

    # Run through model
    output = list(model(processed).values())[0].numpy()
    output = np.squeeze(output)

    if output.shape == (1, 128, 128, 3):
        output = output[0]
    elif output.shape == (1, 1, 128, 3):
        output = output[0, 0]

    original_resized = image.resize((128, 128))
    original_array = np.array(original_resized).astype('float32') / 255.0

    # Enhanced post-processing for better quality (very subtle)
    # Apply minimal enhancement
    output_img = subtle_enhancement(output)
    
    # Convert back to array for metrics calculation
    output_array = np.array(output_img).astype('float32') / 255.0

    # Metrics calculation using the enhanced output
    psnr_value = psnr(original_array, output_array, data_range=1.0)
    ssim_value = ssim(original_array, output_array, data_range=1.0, channel_axis=2)
    mae_value = mean_absolute_error(original_array.flatten(), output_array.flatten())
    mse_value = mean_squared_error(original_array.flatten(), output_array.flatten())

    noise_diff = np.abs(original_array - output_array).flatten()
    hist, bin_edges = np.histogram(noise_diff, bins=20, range=(0, 1))
    hist = (hist / hist.max()).tolist()
    bin_edges = bin_edges[:-1].tolist()

    log_row = {
        "filename": filename,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "psnr": round(float(psnr_value), 4),
        "ssim": round(float(ssim_value), 4),
        "mae": round(float(mae_value), 4),
        "mse": round(float(mse_value), 4)
    }

    log_path = "metrics_log.csv"
    if os.path.exists(log_path):
        df = pd.read_csv(log_path)
        df = pd.concat([df, pd.DataFrame([log_row])], ignore_index=True)
    else:
        df = pd.DataFrame([log_row])
    df.to_csv(log_path, index=False)

    # Convert the enhanced PIL image to base64
    buf = io.BytesIO()
    output_img.save(buf, format='PNG')
    base64_img = base64.b64encode(buf.getvalue()).decode('utf-8')

    return jsonify({
        "image": base64_img,
        "psnr": round(float(psnr_value), 4),
        "ssim": round(float(ssim_value), 4),
        "mae": round(float(mae_value), 4),
        "mse": round(float(mse_value), 4),
        "noise_hist": hist,
        "bin_edges": bin_edges
    })

@app.route('/download_csv')
def download_csv():
    csv_path = "metrics_log.csv"
    if os.path.exists(csv_path):
        return send_file(csv_path, as_attachment=True)
    else:
        return jsonify({"error": "CSV log not found"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)