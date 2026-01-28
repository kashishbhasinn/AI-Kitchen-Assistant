import google.generativeai as genai
import json

# Gemini API Key
GEMINI_API_KEY = ""

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def setup_gemini_model():
    """Set up and return the Gemini model."""
    # Using the Gemini Pro model which is suitable for text generation
    model = genai.GenerativeModel('gemini-pro')
    return model

def generate_recipe(ingredients):
    """
    Generate recipe suggestions based on ingredients using Gemini API.
    
    Args:
        ingredients: List of ingredients
    
    Returns:
        dict: Recipe information including name, description, ingredients, instructions,
              nutritional information, and a fun fact
    """
    model = setup_gemini_model()
    
    # Create a prompt for the Gemini model
    ingredients_text = ", ".join(ingredients)
    prompt = f"""
    I have the following ingredients: {ingredients_text}.
    
    Please generate a recipe that uses these ingredients. Format your response as a JSON object with the following structure:
    {{
        "recipe_name": "Name of the recipe",
        "description": "Brief description of the dish",
        "ingredients": ["List of ingredients with quantities"],
        "instructions": ["Step-by-step cooking instructions"],
        "nutrition": {{
            "calories": "Total calories (e.g., 500 kcal)",
            "protein": "Protein content (e.g., 30g)",
            "carbs": "Carbohydrate content (e.g., 45g)",
            "fat": "Fat content (e.g., 15g)"
        }},
        "fun_fact": "An interesting fact about this dish or one of its ingredients"
    }}
    
    Make sure the recipe is practical, delicious, and uses as many of the provided ingredients as possible.
    Only respond with the JSON object, no additional text.
    """
    
    try:
        # Generate content from Gemini
        response = model.generate_content(prompt)
        
        # Extract the JSON from the response
        response_text = response.text
        
        # Sometimes the model might include markdown code block indicators, remove them
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
            
        # Parse the JSON response
        recipe_data = json.loads(response_text)
        
        return recipe_data
    
    except Exception as e:
        print(f"Error generating recipe with Gemini API: {e}")
        # Return a default error response
        return {
            "recipe_name": "Recipe Generation Failed",
            "description": "We couldn't generate a recipe with the provided ingredients. Please try again.",
            "ingredients": [],
            "instructions": [],
            "nutrition": {
                "calories": "N/A",
                "protein": "N/A",
                "carbs": "N/A",
                "fat": "N/A"
            },
            "fun_fact": "Did you know? The first cookbook was written in 1700 BCE in ancient Mesopotamia."
        }

def generate_fun_fact(dish_name):
    """
    Generate a fun fact about a dish using Gemini API.
    
    Args:
        dish_name: Name of the dish
    
    Returns:
        str: A fun fact about the dish
    """
    model = setup_gemini_model()
    
    prompt = f"""
    Please provide an interesting fun fact about the dish "{dish_name}" or one of its common ingredients.
    The fun fact should be educational, surprising, or entertaining.
    Keep it to 1-2 sentences maximum.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating fun fact with Gemini API: {e}")
        return "Did you know? Humans have been cooking food for at least 250,000 years, transforming ingredients into delicious meals across cultures and generations."
