import streamlit as st
import os
from PIL import Image
import io
import json
from dotenv import load_dotenv

# Import our custom modules
from clarifai_integration import analyze_image
from gemini_integration import generate_recipe, generate_fun_fact

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Recipe Generator",
    page_icon="🍳",
    layout="wide"
)

# App title and description
st.title("🍳 Recipe Generator")
st.markdown("""
This app helps you generate recipe ideas based on ingredients you have available.
Upload an image of your ingredients or enter them as text, and get recipe suggestions with nutritional information and fun facts!
""")

# Create sidebar for app navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "About"])

# Initialize session state for storing results
if 'recipe_data' not in st.session_state:
    st.session_state.recipe_data = None
if 'detected_ingredients' not in st.session_state:
    st.session_state.detected_ingredients = None

def display_recipe(recipe_data):
    """Display the recipe data in a formatted way"""
    if not recipe_data:
        return
    
    st.subheader(recipe_data["recipe_name"])
    st.markdown(recipe_data["description"])
    
    # Create columns for ingredients and instructions
    ingredients_col, instructions_col = st.columns(2)
    with ingredients_col:
        st.markdown("#### Ingredients")
        for ingredient in recipe_data["ingredients"]:
            st.markdown(f"- {ingredient}")
    
    with instructions_col:
        st.markdown("#### Instructions")
        for i, instruction in enumerate(recipe_data["instructions"], 1):
            st.markdown(f"{i}. {instruction}")
    
    # Nutritional information section
    st.subheader("Nutritional Information")
    nutrition_container = st.container()
    with nutrition_container:
        # Create columns for nutritional data
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Calories", value=recipe_data["nutrition"]["calories"])
        with col2:
            st.metric(label="Protein", value=recipe_data["nutrition"]["protein"])
        with col3:
            st.metric(label="Carbs", value=recipe_data["nutrition"]["carbs"])
        with col4:
            st.metric(label="Fat", value=recipe_data["nutrition"]["fat"])
    
    # Fun fact section
    st.subheader("Fun Fact")
    fun_fact_container = st.container()
    with fun_fact_container:
        st.info(recipe_data["fun_fact"])

if page == "Home":
    # Create two columns for input methods
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload Image of Ingredients")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Add a button to analyze the image
            if st.button("Analyze Image"):
                with st.spinner("Analyzing ingredients in the image..."):
                    # Reset the file pointer to the beginning
                    uploaded_file.seek(0)
                    
                    # Call the Clarifai API to analyze the image
                    try:
                        detected_ingredients = analyze_image(uploaded_file)
                        st.session_state.detected_ingredients = detected_ingredients
                        
                        if detected_ingredients:
                            st.success(f"Detected ingredients: {', '.join(detected_ingredients)}")
                            
                            # Generate recipe based on detected ingredients
                            with st.spinner("Generating recipe suggestions..."):
                                recipe_data = generate_recipe(detected_ingredients)
                                st.session_state.recipe_data = recipe_data
                        else:
                            st.warning("No ingredients detected in the image. Please try another image or use text input.")
                    except Exception as e:
                        st.error(f"Error analyzing image: {str(e)}")
    
    with col2:
        st.subheader("Enter Ingredients as Text")
        text_input = st.text_area("List your ingredients (comma separated)", height=100, 
                                placeholder="e.g., chicken, spinach, tomatoes, pasta")
        
        # Add a button to generate recipe from text input
        if st.button("Generate Recipe from Text"):
            if text_input:
                with st.spinner("Processing ingredients..."):
                    # Parse the ingredients from text
                    ingredients_list = [item.strip() for item in text_input.split(',')]
                    st.session_state.detected_ingredients = ingredients_list
                    
                    st.success(f"Ingredients: {', '.join(ingredients_list)}")
                    
                    # Generate recipe based on text ingredients
                    with st.spinner("Generating recipe suggestions..."):
                        try:
                            recipe_data = generate_recipe(ingredients_list)
                            st.session_state.recipe_data = recipe_data
                        except Exception as e:
                            st.error(f"Error generating recipe: {str(e)}")
            else:
                st.warning("Please enter some ingredients first.")
    
    # Display the recipe if available in session state
    if st.session_state.recipe_data:
        display_recipe(st.session_state.recipe_data)
    else:
        # Create placeholder sections when no recipe is available
        st.subheader("Recipe Suggestions")
        st.markdown("Your recipe suggestions will appear here after analysis.")

elif page == "About":
    st.subheader("About This App")
    st.markdown("""
    This Recipe Generator app uses:
    
    - **Clarifai API** for computer vision to detect ingredients in uploaded images
    - **Google Gemini API** for generating recipe suggestions, nutritional information, and fun facts
    - **Streamlit** for the user interface
    
    Created as a demonstration of combining computer vision and natural language processing for practical applications.
    """)
    
    st.subheader("How to Use")
    st.markdown("""
    1. **Upload an image** of your ingredients or **enter them as text**
    2. Click the corresponding button to analyze and generate recipes
    3. View the suggested recipes, nutritional information, and fun facts
    """)
    
    st.subheader("Error Handling")
    st.markdown("""
    - If the image analysis fails to detect ingredients, try uploading a clearer image or use the text input option
    - If you encounter API limits, wait a few minutes and try again
    - For best results, ensure your images clearly show the ingredients
    """)
