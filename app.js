class FoodAnalyzerApp {
    constructor() {
        this.cameraManager = new CameraManager();
        this.chatGPT = new ChatGPTVision();
        this.currentRecipes = [];
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        const startCameraBtn = document.getElementById('startCamera');
        const analyzeBtn = document.getElementById('analyzeBtn');
        const closeRecipeBtn = document.getElementById('closeRecipe');

        startCameraBtn.addEventListener('click', () => this.handleStartCamera());
        analyzeBtn.addEventListener('click', () => this.handleAnalyze());
        closeRecipeBtn.addEventListener('click', () => this.hideRecipeDetails());

        // Enable analyze button when camera is ready
        this.cameraManager.video.addEventListener('loadeddata', () => {
            if (this.cameraManager.isCameraReady()) {
                document.getElementById('analyzeBtn').disabled = false;
            }
        });
    }

    async handleStartCamera() {
        try {
            const startCameraBtn = document.getElementById('startCamera');
            const analyzeBtn = document.getElementById('analyzeBtn');

            startCameraBtn.textContent = '🔄 Starting...';
            startCameraBtn.disabled = true;

            await this.cameraManager.startCamera();

            startCameraBtn.textContent = '📷 Camera Active';
            startCameraBtn.style.background = '#28A745';
            analyzeBtn.disabled = false;

            this.hideError();
        } catch (error) {
            this.showError(error.message);
            const startCameraBtn = document.getElementById('startCamera');
            startCameraBtn.textContent = '📷 Start Camera';
            startCameraBtn.disabled = false;
        }
    }

    async handleAnalyze() {
        if (!this.cameraManager.isCameraReady()) {
            this.showError('Camera is not ready. Please start the camera first.');
            return;
        }

        try {
            this.showAnalysisSection();
            this.showLoading();

            // Capture image from camera
            const imageData = this.cameraManager.captureImage();

            // Analyze with ChatGPT Vision
            const analysis = await this.chatGPT.analyzeFood(imageData);

            this.currentRecipes = analysis.recipes;
            this.displayResults(analysis);

        } catch (error) {
            this.showError(error.message);
            this.hideAnalysisSection();
        }
    }

    showAnalysisSection() {
        document.getElementById('analysisSection').style.display = 'block';
        document.getElementById('results').style.display = 'none';
        document.getElementById('loading').style.display = 'block';
    }

    showLoading() {
        document.getElementById('loading').style.display = 'block';
        document.getElementById('results').style.display = 'none';
    }

    displayResults(analysis) {
        const loading = document.getElementById('loading');
        const results = document.getElementById('results');
        const detectedFoods = document.getElementById('detectedFoods');
        const recipeButtons = document.getElementById('recipeButtons');

        // Hide loading, show results
        loading.style.display = 'none';
        results.style.display = 'block';

        // Display detected foods
        detectedFoods.innerHTML = '';
        analysis.detectedFoods.forEach(food => {
            const foodTag = document.createElement('span');
            foodTag.className = 'food-tag';
            foodTag.textContent = food;
            detectedFoods.appendChild(foodTag);
        });

        // Display recipe buttons
        recipeButtons.innerHTML = '';
        analysis.recipes.forEach((recipe, index) => {
            const recipeBtn = document.createElement('button');
            recipeBtn.className = 'recipe-btn';
            recipeBtn.innerHTML = `
                <strong>${recipe.title}</strong><br>
                <small>${recipe.description}</small>
            `;
            recipeBtn.addEventListener('click', () => this.showRecipeDetails(index));
            recipeButtons.appendChild(recipeBtn);
        });

        // Simulate voice description (in a real app, this would use ChatGPT Voice API)
        this.simulateVoiceDescription(analysis);
    }

    simulateVoiceDescription(analysis) {
        // In a real app, this would call ChatGPT Voice API
        // For demo purposes, we'll just show a message
        const voiceMessage = `I can see ${analysis.detectedFoods.join(', ')} in your image. Here are 3 delicious recipes you can make with these ingredients!`;
        
        // Create a temporary voice message display
        const voiceDiv = document.createElement('div');
        voiceDiv.className = 'voice-message';
        voiceDiv.style.cssText = `
            background: #E8F5E8;
            color: #2E7D32;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
            font-style: italic;
        `;
        voiceDiv.textContent = `🎤 "${voiceMessage}"`;
        
        const results = document.getElementById('results');
        results.insertBefore(voiceDiv, results.firstChild);
    }

    showRecipeDetails(recipeIndex) {
        const recipe = this.currentRecipes[recipeIndex];
        const recipeTitle = document.getElementById('recipeTitle');
        const recipeContent = document.getElementById('recipeContent');
        const recipeDetails = document.getElementById('recipeDetails');

        recipeTitle.textContent = recipe.title;
        
        let contentHTML = `
            <div class="recipe-content">
                <p><strong>Description:</strong> ${recipe.description}</p>
                
                <h4>Ingredients:</h4>
                <ul>
                    ${recipe.ingredients.map(ingredient => `<li>${ingredient}</li>`).join('')}
                </ul>
                
                <h4>Instructions:</h4>
                <ol>
                    ${recipe.instructions.map(instruction => `<li>${instruction}</li>`).join('')}
                </ol>
            </div>
        `;
        
        recipeContent.innerHTML = contentHTML;
        recipeDetails.style.display = 'block';
        
        // Scroll to recipe details
        recipeDetails.scrollIntoView({ behavior: 'smooth' });
    }

    hideRecipeDetails() {
        document.getElementById('recipeDetails').style.display = 'none';
    }

    hideAnalysisSection() {
        document.getElementById('analysisSection').style.display = 'none';
    }

    showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        
        // Auto-hide error after 5 seconds
        setTimeout(() => {
            this.hideError();
        }, 5000);
    }

    hideError() {
        document.getElementById('errorMessage').style.display = 'none';
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FoodAnalyzerApp();
});