# Face Deblurring Web App 🚀

A deep learning-based web application for deblurring low-quality face images using a CBAM-enhanced U-Net architecture. The app performs image restoration, applies quality enhancement (CLAHE, denoising, unsharp masking), and computes evaluation metrics such as PSNR, SSIM, MAE, and MSE.

---

## 🔧 Features

- ✅ Upload blurred face images (selfies or low-light images)
- ✅ Preprocessing pipeline with:
  - CLAHE (Contrast Limited Adaptive Histogram Equalization)
  - Mild denoising (FastNlMeansDenoisingColored)
  - Unsharp masking
  - Adaptive contrast and sharpness tuning
- ✅ Real-time deblurring using a TensorFlow SavedModel (`TFSMLayer`)
- ✅ Visualization of:
  - PSNR (Peak Signal-to-Noise Ratio)
  - SSIM (Structural Similarity Index)
  - MAE and MSE
  - Noise difference histogram (intensity loss vs. enhancement)
- ✅ CSV log export of metrics for uploaded images
- ✅ Web-Based UI (Three.js, Daisy UI, Lenis UI)
- ✅ Clear separation of routes for `/` (landing) and `/in` (deblurring)

---

## 🧠 Model Overview

- **Architecture:** U-Net with CBAM (Convolutional Block Attention Module)
- **Loss Function:** Perceptual + Pixel Loss
- **Trained On:** Human face datasets (with synthetic blur)
- **Resolution:** 128×128 input/output
- **Inference Layer:** `TFSMLayer` from Keras (`autoencoder_model/`)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/bhuvan2018/Enhancing_Image_Clarity_Denoising_Autoencoder.git
cd Enhancing_Image_Clarity_Denoising_Autoencoder
````

### 2. Install Requirements

```bash
pip install -r requirements.txt

### 3. Folder Structure

```
├── app.py
├── autoencoder_model/         # Trained SavedModel (TensorFlow)
├── templates/
│   ├── home.html              # Landing page
│   └── index.html             # Upload & deblur interface
├── static/uploads/           # Uploaded images
├── metrics_log.csv           # Log of processed images and metrics
└── README.md
```

### 4. Run the App

```bash
python app.py
```

Navigate to:

* `http://127.0.0.1:5000/` → Home
* `http://127.0.0.1:5000/in` → Deblurring Interface

---

## 📊 Sample Metrics (on output images)

| Image        | PSNR (dB) | SSIM | MAE   | MSE    |
| ------------ | --------- | ---- | ----- | ------ |
| `blur1.jpg`  | 27.42     | 0.86 | 0.031 | 0.0021 |
| `blur2.jpg`  | 28.13     | 0.88 | 0.028 | 0.0017 |
| `mobile.jpg` | 25.60     | 0.75 | 0.045 | 0.0034 |

---

## 📦 Deployment

SOON.....

---

## 📁 Dataset & Training

* **Dataset:** celeba faces
* **Augmentation:** Gaussian + Motion blur
* **Training:** Custom CBAM-U-Net + Multi-scale loss (Perceptual + Pixel)

---

## ✍️ Author

**Bhuvan Shetty**
📧 \[bhuvanshetty2018@gmail.com]
📌 Built with ❤️ using Three.js, Daisy, Lenis, TensorFlow, Flask
---
