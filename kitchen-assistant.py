import openai as genai
import streamlit as st

# Configure the API key
genai.configure(api_key="AIzaSyAH7X3jMH_GQ0XFiwNZHdrjsavzDOe293Q")  

# Function to get the response from the Gemini model
def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI setup
st.markdown("<h1 style='text-align: center;'>🤖 Welcome to AI Kitchen Assistant</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Get detailed information about your food!</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Your AI assistant is here to help you! 🚀</p>", unsafe_allow_html=True)

# Sidebar setup
st.sidebar.header("**A Project by Kashish Bhasin**")
st.sidebar.write("AI & ML Student")

st.sidebar.header("Contact Information", divider='rainbow')
st.sidebar.write("Feel free to reach out through the following")
st.sidebar.write("[LinkedIn](linkedin.com/in/kashish-bhasin)")
st.sidebar.write("[GitHub](https://github.com/kashishbhasinn)")
st.sidebar.write("[Email](mailto:kashishbhasinn@gmail.com)")
st.sidebar.write("Developed by Kashish Bhasin", unsafe_allow_html=True)
# Input field for the ingredient
ingredient = st.text_area("Enter your ingredient")

# Buttons for different functionalities
submit = st.button("Nutritional content")
submit1 = st.button("Dishes to Create")
submit2 = st.button("Fun Fact")

# Process the button clicks and generate the appropriate responses
if submit:
    prompt = f"Provide a detailed nutritional analysis for the ingredient {ingredient}. Include the amounts of macronutrients (proteins, fats, carbohydrates) and micronutrients (vitamins and minerals) per 100 grams. Highlight any significant health benefits or risks associated with these nutrients."
    response = get_gemini_response(prompt)
    st.subheader("Nutritional Content")
    st.write(response)

if submit1:
    prompt1 = f"Suggest a variety of dishes that can be made using {ingredient} as the main ingredient. Include a brief description of each dish and highlight any popular or traditional recipes."
    response1 = get_gemini_response(prompt1)
    st.subheader("Dishes to Create")
    st.write(response1)

if submit2:
    prompt2 = f"Share an interesting or fun fact about the ingredient {ingredient}. This could include its history, cultural significance, unusual uses, or any surprising nutritional information."
    response2 = get_gemini_response(prompt2)
    st.subheader("Fun Fact")
    st.write(response2)
