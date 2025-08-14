class ChatGPTVision {
    constructor() {
        // Note: In a real app, you'd need to set up your own backend with API key
        // For demo purposes, we'll simulate the API response
        this.apiEndpoint = 'https://api.openai.com/v1/chat/completions';
        this.apiKey = null; // Set this in production
    }

    async analyzeFood(imageDataUrl) {
        try {
            // For demo purposes, we'll simulate the API call
            // In production, you'd send the image to ChatGPT Vision API
            
            // Simulate API delay
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // Demo response - replace with actual API call
            return this.getDemoResponse();
            
        } catch (error) {
            console.error('Error analyzing food:', error);
            throw new Error('Failed to analyze food image');
        }
    }

    getDemoResponse() {
        // This is a demo response - replace with actual ChatGPT Vision API call
        const demoFoods = [
            'tomatoes', 'onions', 'garlic', 'olive oil', 'pasta'
        ];
        
        const demoRecipes = [
            {
                title: 'Classic Marinara Pasta',
                description: 'A simple and delicious tomato-based pasta sauce',
                ingredients: [
                    '2 cups fresh tomatoes, diced',
                    '1 medium onion, finely chopped',
                    '3 cloves garlic, minced',
                    '2 tbsp olive oil',
                    '1 lb pasta of your choice',
                    'Salt and pepper to taste',
                    'Fresh basil leaves'
                ],
                instructions: [
                    'Bring a large pot of salted water to boil and cook pasta according to package directions.',
                    'In a large skillet, heat olive oil over medium heat.',
                    'Add chopped onions and cook until translucent, about 5 minutes.',
                    'Add minced garlic and cook for 1 minute until fragrant.',
                    'Add diced tomatoes and cook for 10-15 minutes until they break down.',
                    'Season with salt and pepper to taste.',
                    'Toss cooked pasta with the sauce and garnish with fresh basil.'
                ]
            },
            {
                title: 'Roasted Tomato Soup',
                description: 'A warm and comforting soup perfect for any season',
                ingredients: [
                    '6 large tomatoes, halved',
                    '2 onions, quartered',
                    '4 cloves garlic, unpeeled',
                    '3 tbsp olive oil',
                    '4 cups vegetable broth',
                    'Salt and pepper to taste',
                    'Fresh herbs for garnish'
                ],
                instructions: [
                    'Preheat oven to 400°F (200°C).',
                    'Place tomatoes, onions, and garlic on a baking sheet.',
                    'Drizzle with olive oil and season with salt and pepper.',
                    'Roast for 30-35 minutes until vegetables are caramelized.',
                    'Remove from oven and let cool slightly.',
                    'Transfer to a blender and add vegetable broth.',
                    'Blend until smooth and return to pot.',
                    'Heat through and adjust seasoning as needed.'
                ]
            },
            {
                title: 'Fresh Tomato Salsa',
                description: 'A vibrant and fresh salsa perfect for dipping or topping',
                ingredients: [
                    '4 medium tomatoes, diced',
                    '1 small onion, finely chopped',
                    '2 cloves garlic, minced',
                    '1 lime, juiced',
                    '1/4 cup fresh cilantro, chopped',
                    'Salt and pepper to taste',
                    'Optional: jalapeño for heat'
                ],
                instructions: [
                    'In a medium bowl, combine diced tomatoes and chopped onion.',
                    'Add minced garlic and fresh cilantro.',
                    'Squeeze in lime juice and season with salt and pepper.',
                    'Mix gently to combine all ingredients.',
                    'Let sit for 15 minutes to allow flavors to meld.',
                    'Taste and adjust seasoning as needed.',
                    'Serve immediately or refrigerate for up to 2 days.'
                ]
            }
        ];

        return {
            detectedFoods: demoFoods,
            recipes: demoRecipes
        };
    }

    // For production use, implement actual ChatGPT Vision API call:
    async callChatGPTVisionAPI(imageDataUrl) {
        // Convert base64 to blob
        const response = await fetch(imageDataUrl);
        const blob = await response.blob();
        
        // Create form data
        const formData = new FormData();
        formData.append('image', blob, 'food.jpg');
        formData.append('prompt', 'Analyze this image and identify all visible food items. Then suggest 3 different recipes that can be made using these ingredients. For each recipe, provide a title, description, ingredients list, and step-by-step instructions.');
        
        // Make API call to your backend
        const apiResponse = await fetch('/api/analyze-food', {
            method: 'POST',
            body: formData
        });
        
        if (!apiResponse.ok) {
            throw new Error('API request failed');
        }
        
        return await apiResponse.json();
    }
}