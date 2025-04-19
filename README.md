# Recipe Generator App

A Streamlit application that uses Clarifai (Computer Vision) and Google Gemini (NLP) to generate recipes based on ingredients detected in images or entered as text.

## Features

- **Ingredient Detection**: Upload images of ingredients and detect them using Clarifai's computer vision API
- **Recipe Generation**: Generate recipe ideas based on available ingredients using Google Gemini
- **Nutritional Information**: Get nutritional content (calories, macros, etc.) for each recipe
- **Fun Facts**: Learn interesting facts about the dishes or ingredients

## How to Use

1. **Upload an Image**: Take a photo of your ingredients and upload it to the app
2. **Or Enter Ingredients as Text**: Type in the ingredients you have available
3. **Generate Recipe**: Click the button to analyze and generate recipe suggestions
4. **View Results**: See the suggested recipes, nutritional information, and fun facts

## Installation

To run this app locally:

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## API Keys

The app uses the following APIs:
- Clarifai API for computer vision (API Key is included in the code)
- Google Gemini API for recipe generation (API Key is included in the code)

## Deployment

This app is ready to be deployed on Streamlit Sharing. Simply connect your GitHub repository to Streamlit Sharing and it will automatically deploy the app.

## Limitations

- English language only
- No user accounts or history
- No dietary filters (all recipes welcome)

## Credits

This app was created as a demonstration of combining computer vision and natural language processing for practical applications.
