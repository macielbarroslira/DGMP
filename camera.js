class CameraManager {
    constructor() {
        this.video = document.getElementById('camera');
        this.canvas = document.getElementById('canvas');
        this.stream = null;
        this.isActive = false;
    }

    async startCamera() {
        try {
            const constraints = {
                video: {
                    facingMode: 'environment', // Use back camera on mobile
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                }
            };

            this.stream = await navigator.mediaDevices.getUserMedia(constraints);
            this.video.srcObject = this.stream;
            this.isActive = true;
            
            return true;
        } catch (error) {
            console.error('Error accessing camera:', error);
            throw new Error('Unable to access camera. Please ensure camera permissions are granted.');
        }
    }

    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
            this.isActive = false;
        }
    }

    captureImage() {
        if (!this.isActive) {
            throw new Error('Camera is not active');
        }

        const context = this.canvas.getContext('2d');
        this.canvas.width = this.video.videoWidth;
        this.canvas.height = this.video.videoHeight;
        
        context.drawImage(this.video, 0, 0);
        
        return this.canvas.toDataURL('image/jpeg', 0.8);
    }

    isCameraReady() {
        return this.isActive && this.video.readyState >= 2;
    }
}