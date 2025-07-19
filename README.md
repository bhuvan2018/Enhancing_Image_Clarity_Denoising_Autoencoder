# Face Deblurring Web App 🚀

A deep learning-powered web application to **restore low-quality or blurred face images** using a **CBAM-enhanced U-Net** architecture. The system performs intelligent image enhancement through CLAHE, denoising, and unsharp masking — and provides detailed evaluation metrics including PSNR, SSIM, MAE, and MSE.

---

## 🔍 Key Features

- 📤 Upload blurry face images (e.g., selfies, low-light portraits)
- 🧪 Preprocessing pipeline with:
  - CLAHE (Contrast Limited Adaptive Histogram Equalization)
  - FastNlMeansDenoisingColored (light denoising)
  - Unsharp masking
  - Adaptive sharpness & contrast adjustment
- 🧠 Real-time deblurring with **TensorFlow SavedModel** via `TFSMLayer`
- 📊 Metrics Visualization:
  - PSNR (Peak Signal-to-Noise Ratio)
  - SSIM (Structural Similarity Index)
  - MAE, MSE
  - Noise Difference Histogram (Intensity Loss vs. Enhancement)
- 📥 CSV log export of image metrics
- 🌐 Web UI with:
  - Landing page (`/`)
  - Deblurring interface (`/in`)
- 💻 Frontend stack: **Three.js**, **Daisy UI**, **Lenis UI**

---

## 🧠 Model Overview

- **Architecture:** U-Net with CBAM (Convolutional Block Attention Module)
- **Loss Function:** Perceptual + Pixel Loss (Multi-Scale)
- **Input/Output Size:** 128 × 128
- **Trained On:** Human face datasets with synthetic blur (Gaussian + Motion)
- **Deployment Format:** TensorFlow SavedModel (`autoencoder_model/`)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/bhuvan2018/Enhancing_Image_Clarity_Denoising_Autoencoder.git
cd Enhancing_Image_Clarity_Denoising_Autoencoder
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Project Structure

```
├── app.py                     # Flask backend
├── autoencoder_model/         # Trained TensorFlow SavedModel
├── templates/
│   ├── home.html              # Landing page
│   └── index.html             # Deblurring interface
├── static/uploads/            # Uploaded images
├── metrics_log.csv            # Metrics log for processed images
└── README.md
```

### 4. Run Locally

```bash
python app.py
```

Open in browser:

* `http://127.0.0.1:5000/` → Home
* `http://127.0.0.1:5000/in` → Deblurring UI

---

## 📊 Sample Output Metrics

| Image        | PSNR (dB) | SSIM | MAE   | MSE    |
| ------------ | --------- | ---- | ----- | ------ |
| `blur1.jpg`  | 27.42     | 0.86 | 0.031 | 0.0021 |
| `blur2.jpg`  | 28.13     | 0.88 | 0.028 | 0.0017 |
| `mobile.jpg` | 25.60     | 0.75 | 0.045 | 0.0034 |

---

## 📦 Deployment

> ⚙️ Deployment instructions via **Render / Docker / Gunicorn** coming soon...

---

## 📁 Dataset & Training Details

* **Dataset Used:** CelebA Faces + Human Faces Dataset
* **Blur Types:** Randomized Gaussian and Motion Blur (synthetically added)
* **Training Pipeline:**

  * CBAM-enhanced U-Net
  * Perceptual + Pixel loss (multi-scale)
  * Trained using 128×128 face crops

---

## 🙋‍♂️ Author

**Bhuvan Shetty**
📧 \[[bhuvanshetty2018@gmail.com](mailto:bhuvanshetty2018@gmail.com)]
Built with ❤️ using Flask, TensorFlow, Three.js, DaisyUI & Lenis

---

```
