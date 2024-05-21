const imageInput = document.getElementById("image-input");
const uploadBtn = document.getElementById("upload-btn");
const originalImageElement = document.getElementById("original-image");
const segmentedImageElement = document.getElementById("segmented-image");
const predictedAreaElement = document.getElementById("predicted-area");
const executionTimeValue = document.getElementById("execution-time-value");

uploadBtn.addEventListener("click", async () => {
    const file = imageInput.files[0];
    if (!file) {
        alert("Vui lòng chọn một ảnh");
        return;
    }

    const formData = new FormData();
    formData.append("image", file);

    try {
        const response = await fetch("/segment", {
        method: "POST",
        body: formData,
        });

        const data = await response.json();
        const segmentedImageData = new Uint8Array(data.segmented_image);
        const segmentedImageBlob = new Blob([segmentedImageData], {
        type: "image/png",
        });
        const segmentedImageUrl = URL.createObjectURL(segmentedImageBlob);

        originalImageElement.src = URL.createObjectURL(file);
        segmentedImageElement.src = segmentedImageUrl;
        predictedAreaElement.textContent = data.area;
        executionTimeValue.textContent = data.execution_time;
    } catch (error) {
        console.error("Error:", error);
    }
});

document.getElementById("logout-btn").addEventListener("click", function() {
    window.location.href = "/";
});