import streamlit as st
from streamlit_lottie import st_lottie
import json

def load_lottie(filepath: str):
    """
    Load a Lottie JSON file from a given filepath.
    """
    with open(filepath, "r") as file:
        return json.load(file)

def display_header():
    """
    Displays the header section of the Streamlit app, including the logo, title, and Lottie animation.
    """
    # Import custom font using Google Fonts
    
    # st.markdown(
    #     """
    #     <style>
    #         /* Load font from Google Fonts */
    #         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200&display=swap');

    #         /* Apply font to body */
    #         html, body, [class*="css"] {
    #             font-family: 'Inter', sans-serif !important;
    #         }

    #         .custom-title {
    #             font-family: 'Inter', sans-serif;
    #             font-size: 2.5rem;
    #             font-weight: 200; /* Light weight */
    #             background: linear-gradient(to right, #ffc44d, white);
    #             -webkit-background-clip: text;
    #             -webkit-text-fill-color: transparent;
    #             margin: 7px 0 0 0;
    #         }
    #     </style>
    #     """,
    #     unsafe_allow_html=True,
    # )
    

    # Load the Lottie file
    lottie_path = "assets/lottie/Hexagone Loader.json"
    lottie_loader = load_lottie(lottie_path)

    # Set the logo in the header navbar
    st.logo(
        "assets/images/ava_logo.png",  # Path to your logo file
        size="large",
    )

    # Display the title with the Lottie animation on the left
    col1, col2 = st.columns([1, 6])  # Adjust the column widths as needed

    with col1:
        st_lottie(lottie_loader, height=100, width=100, key="title_loader")  # Display the Lottie animation

    with col2:
        st.markdown('<h1 class="custom-title">Agentic Investment Insights</h1>', unsafe_allow_html=True)  # Custom styled title
