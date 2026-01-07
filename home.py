import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

st.set_page_config(page_title="StudyGen.AI", page_icon="📚", layout="centered") # layout="wide" for more space

st.title("📚 StudyGen.AI")
st.subheader("Your AI-powered study buddy")

# Using columns for a more engaging intro
col1, col2 = st.columns([2, 3]) # Adjust column ratios

with col1:
    st.markdown("""
    Welcome to **StudyGen.AI**, your all-in-one academic toolkit powered by advanced LLMs.

    Unlock smarter learning with:
    - 📅 **Study Planner:** Organize your study schedule.
    - 🧠 **Flashcards:** Master key concepts with ease.
    - ❓ **Quiz Generator:** Test your knowledge effectively.
    - 🎮 **Algorithm Games:** Learn through interactive puzzles.
    """)

with col2:
    # You could add an image here for visual appeal
    # st.image("path/to/your/study_image.png", use_column_width=True)
    # For now, let's keep it simple or add a little more text
    st.info("💡 **Tip:** Explore each tool via the navigation in the sidebar. Simply select a feature to get started!")

st.divider() # Visual separation

st.markdown("""
### How it Works:
StudyGen.AI leverages cutting-edge Large Language Models (LLMs) to transform your raw study materials into structured, personalized learning aids. Just provide your content, and let AI do the heavy lifting!
""")

st.write("Ready to transform your study routine? Choose a tool from the sidebar!")

# Footer (optional but good for branding)
st.markdown("---")
st.markdown("Created with ❤️ by StudyGen.AI Team")