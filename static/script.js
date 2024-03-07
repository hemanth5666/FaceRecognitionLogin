const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture-btn');
const context = canvas.getContext('2d');

async function setupCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        await new Promise(resolve => video.onloadedmetadata = resolve);
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
    } catch (err) {
        console.error('Error accessing webcam: ', err);
    }
}

async function captureImage() {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/jpeg');
    try {
        const response = await fetch('/recognize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image_data: imageData })
        });
        const result = await response.json();
        if (result.success) {
            window.location.href = '/welcome'; // Redirect to welcome page upon successful recognition
        } else {
            alert('Face not recognized. Please try again.');
        }
    } catch (error) {
        console.error('Error capturing image or sending request: ', error);
        alert('An error occurred. Please try again later.');
    }
}

window.onload = () => {
    setupCamera();
    captureButton.onclick = captureImage;
};





