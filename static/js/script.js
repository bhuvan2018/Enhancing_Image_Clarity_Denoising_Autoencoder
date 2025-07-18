// === Image upload + prediction handler ===
document.getElementById("upload-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const imageInput = document.getElementById("image");
  const imageFile = imageInput.files[0];
  if (!imageFile) return;

  const originalPreview = document.getElementById("inputPreview");
  originalPreview.src = URL.createObjectURL(imageFile);
  originalPreview.style.display = "block";

  const loading = document.getElementById("loading");
  loading.style.display = "block";

  const outputImg = document.getElementById("output-img");
  const downloadBtn = document.getElementById("downloadBtn");
  const metricsDiv = document.getElementById("metrics");
  const chartContainer = document.getElementById("chart-container");
  const noiseChartContainer = document.getElementById("noise-chart-container");
  outputImg.style.display = "none";
  downloadBtn.style.display = "none";
  metricsDiv.style.display = "none";
  chartContainer.style.display = "none";
  noiseChartContainer.style.display = "none";

  document.getElementById("psnr-value").textContent = "";
  document.getElementById("ssim-value").textContent = "";
  document.getElementById("mae-value").textContent = "";
  document.getElementById("mse-value").textContent = "";

  const formData = new FormData();
  formData.append("image", imageFile);

  fetch("/predict", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      const base64Image = data.image;
      const psnr = parseFloat(data.psnr).toFixed(2);
      const ssim = parseFloat(data.ssim).toFixed(4);
      const mae = parseFloat(data.mae).toFixed(4);
      const mse = parseFloat(data.mse).toFixed(4);
      const noiseHist = data.noise_hist;
      const binEdges = data.bin_edges;

      outputImg.src = `data:image/png;base64,${base64Image}`;
      outputImg.style.display = "block";

      document.getElementById("psnr-value").textContent = psnr;
      document.getElementById("ssim-value").textContent = ssim;
      document.getElementById("mae-value").textContent = mae;
      document.getElementById("mse-value").textContent = mse;
      metricsDiv.style.display = "block";

      chartContainer.style.display = "block";
      drawMetricChart(psnr, ssim, mae, mse);

      if (noiseHist && binEdges) {
        noiseChartContainer.style.display = "block";
        drawNoiseHistogram(noiseHist, binEdges);
      }

      const blob = b64toBlob(base64Image, "image/png");
      const blobUrl = URL.createObjectURL(blob);
      downloadBtn.href = blobUrl;
      downloadBtn.style.display = "inline-block";

      loading.style.display = "none";
    })
    .catch((error) => {
      console.error("Error:", error);
      loading.style.display = "none";
      alert("Something went wrong. Please try again.");
    });
});

// === Convert base64 to Blob ===
function b64toBlob(b64Data, contentType = "", sliceSize = 512) {
  const byteCharacters = atob(b64Data);
  const byteArrays = [];

  for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
    const slice = byteCharacters.slice(offset, offset + sliceSize);
    const byteNumbers = Array.from(slice, (char) => char.charCodeAt(0));
    byteArrays.push(new Uint8Array(byteNumbers));
  }

  return new Blob(byteArrays, { type: contentType });
}

// === Comparison Metrics Chart ===
function drawMetricChart(psnr, ssim, mae, mse) {
  const ctx = document.getElementById("comparisonChart").getContext("2d");

  if (window.metricChartInstance) {
    window.metricChartInstance.destroy();
  }

  window.metricChartInstance = new Chart(ctx, {
    type: "pie",
    data: {
      labels: ["PSNR", "SSIM", "MAE", "MSE"],
      datasets: [{
        label: "Metric Values",
        data: [psnr, ssim, mae, mse],
        backgroundColor: [
          "#007bff",  // PSNR - Blue
          "#28a745",  // SSIM - Green
          "#ffc107",  // MAE - Yellow
          "#dc3545"   // MSE - Red
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      aspectRatio: 1,
      plugins: {
        legend: {
          position: "bottom"
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              return `${context.label}: ${context.parsed.toFixed(4)}`;
            }
          }
        }
      }
    }
  });
}


// === Noise Histogram Chart ===
function drawNoiseHistogram(hist, bins) {
  const ctx = document.getElementById("noiseChart").getContext("2d");

  if (window.noiseChartInstance) {
    window.noiseChartInstance.destroy();
  }

  const midpoints = [];
  for (let i = 0; i < bins.length - 1; i++) {
    midpoints.push(((bins[i] + bins[i + 1]) / 2).toFixed(3));
  }

  window.noiseChartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: midpoints,
      datasets: [{
        label: "Noise Pixel Count",
        data: hist,
        backgroundColor: "#17a2b8",
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      aspectRatio: 1,
      scales: {
        x: {
          title: {
            display: true,
            text: "Noise Intensity"
          }
        },
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Pixel Count"
          }
        },
      },
    },
  });
}

// === Modal Logic ===
const modal = document.getElementById("projectModal");
const openBtn = document.getElementById("openModalBtn");
const closeBtn = document.querySelector(".close");

if (modal && openBtn && closeBtn) {
  openBtn.addEventListener("click", () => {
    modal.style.display = "block";
  });

  closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });

  window.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
}
