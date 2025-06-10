import streamlit as st
from utils import call_gpt # Assuming utils.py is correctly structured

st.title("🧠 AI Flashcard Generator")
st.markdown("Paste your topic or syllabus content below, and let AI create instant flashcards for you!")

# Input Area
notes = st.text_area(
    "📚 Your Study Content:",
    height=250,
    placeholder="E.g., 'Photosynthesis: process by which green plants use sunlight to synthesize foods from carbon dioxide and water...'"
)

# Button with enhanced styling
if st.button("✨ Generate Flashcards", use_container_width=True, type="primary"):
    if notes: # Check if input is not empty
        with st.spinner("Generating powerful flashcards... This might take a moment."):
            prompt = f"Create 5 concise flashcards in 'Term - Definition' format, one per line. Ensure terms are bold and definitions are clear. Focus on key concepts from the following:\n\n{notes}"
            response = call_gpt(prompt)

        if response and "Error:" not in response: # Check for AI response errors
            st.success("Flashcards generated successfully!")
            st.markdown("---") # Separator before flashcards

            flashcards = []
            for line in response.split("\n"):
                if " - " in line:
                    parts = line.split(" - ", 1) # Split only on the first ' - '
                    if len(parts) == 2:
                        flashcards.append((parts[0].strip(), parts[1].strip()))
                # Try to handle lines that might not strictly follow "Term - Definition" but are still valid
                elif line.strip() and not line.strip().startswith("Answer:"): # Exclude potential quiz answers
                    flashcards.append((line.strip(), "No explicit definition provided by AI for this line."))


            if flashcards:
                st.subheader("Your Generated Flashcards:")
                for i, (term, definition) in enumerate(flashcards):
                    with st.expander(f"🃏 Flashcard {i+1}: **{term}**"): # Bold term in expander
                        st.write(definition)
            else:
                st.warning("Could not parse flashcards from the AI response. Please try with different content or regenerate.")
                st.code(response) # Show raw response for debugging
        else:
            st.error("Failed to generate flashcards. Please try again or check your API key.")
    else:
        st.warning("Please paste some content into the text area to generate flashcards.")

# Optional: Add a section for tips on writing good notes
st.markdown("---")
st.info("💡 **Tip for best results:** Provide clear, structured notes or syllabus content. The more focused your input, the better your flashcards will be!")