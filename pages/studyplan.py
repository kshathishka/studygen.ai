import streamlit as st
from utils import call_gpt # Assuming utils.py is correctly structured

st.title("📅 AI Study Plan Generator")
st.markdown("Paste your course syllabus or a list of topics, and get a personalized 2-week study plan.")

syllabus = st.text_area(
    "📋 Your Syllabus/Topics:",
    height=300,
    placeholder="E.g., 'Week 1: Introduction to Calculus, Limits, Continuity. Week 2: Derivatives, Chain Rule...'"
)

if st.button("🗓️ Generate Study Plan", use_container_width=True, type="primary"):
    if syllabus:
        with st.spinner("Crafting your optimized study schedule..."):
            prompt = f"""Break down the following syllabus/content into a detailed, day-by-day 2-week study plan.
            Each day should have a clear topic or set of tasks. Use bold for day headers and key topics.
            Format like this:

            Day 1: [Topic/Task]
            - [Detail 1]
            - [Detail 2]

            Day 2: [Topic/Task]
            - [Detail 1]
            - [Detail 2]

            ...and so on for 14 days.

            Syllabus:
            {syllabus}
            """
            plan = call_gpt(prompt)

        if plan and "Error:" not in plan:
            st.success("Study plan generated!")
            st.markdown("---") # Separator

            st.subheader("Your 2-Week Study Plan:")
            
            # Splitting by "Day " ensures we catch the start of each day
            days = plan.split("Day ")
            
            # Iterate through the split parts, skipping the first element if it's empty
            for day_content in days:
                if day_content.strip(): # Ensure the content is not just empty space
                    # Try to parse the day number/header and content
                    lines = day_content.strip().split("\n", 1) # Split only on the first newline
                    if len(lines) > 0:
                        header = lines[0].strip()
                        details = lines[1].strip() if len(lines) > 1 else "No details provided for this day."
                        
                        if header: # Only show expander if header exists
                            with st.expander(f"📘 **Day {header}**"): # Bold the Day header in expander
                                st.markdown(details)
                        else:
                            st.markdown(f"**Day (unspecified):**\n{details}") # Handle potential missing Day number
            if not days or (len(days) == 1 and not days[0].strip()):
                st.warning("Could not parse study plan. Please ensure the AI response follows the 'Day X:' format.")
                st.code(plan) # Show raw plan for debugging
        else:
            st.error("Failed to generate study plan. Please try again or check your API key.")
    else:
        st.warning("Please paste your syllabus or topics into the text area to generate a study plan.")

st.markdown("---")
st.info("💡 **Tip:** The more specific your syllabus, the more detailed and useful your study plan will be!")