import streamlit as st
from utils import call_gpt # Assuming utils.py is correctly structured

st.title("❓ AI Quiz Generator")
st.markdown("Enter your topic or content to generate multiple-choice questions and test your understanding.")

topic = st.text_area(
    "📝 Content for Quiz:",
    height=250,
    placeholder="E.g., 'History of World War II: Causes, major events, key figures, and outcomes...'"
)

# Use session state to store quiz questions and answers
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'quiz_generated' not in st.session_state:
    st.session_state.quiz_generated = False

if st.button("🚀 Generate Quiz", use_container_width=True, type="primary"):
    if topic:
        with st.spinner("Crafting challenging questions..."):
            prompt = f"""Generate 5 multiple-choice questions (MCQs) based on the following content.
            Each question should have:
            - The question text.
            - Four options (A, B, C, D) on separate lines.
            - The correct answer explicitly stated as 'Answer: X' on a new line.

            Example format:
            What is the capital of France?
            A. Berlin
            B. Madrid
            C. Paris
            D. Rome
            Answer: C

            Content:
            {topic}
            """
            raw = call_gpt(prompt)

        if raw and "Error:" not in raw:
            st.session_state.questions = []
            st.session_state.user_answers = {}
            parsed_questions = raw.strip().split("\n\n")

            for i, q_block in enumerate(parsed_questions):
                lines = q_block.strip().split("\n")
                if len(lines) >= 5 and "Answer:" in lines[-1]: # Ensure enough lines and an answer
                    question = lines[0]
                    options = lines[1:-1] # All lines except the last one (answer)
                    answer_line = lines[-1]
                    correct_match = answer_line.split("Answer:")[-1].strip().upper()
                    
                    if correct_match in ["A", "B", "C", "D"]:
                        st.session_state.questions.append({
                            "question": question,
                            "options": options,
                            "correct_answer": correct_match
                        })
            if st.session_state.questions:
                st.session_state.quiz_generated = True
                st.success(f"Quiz generated with {len(st.session_state.questions)} questions!")
            else:
                st.warning("Could not parse quiz questions from the AI response. Please try with different content or regenerate.")
                st.code(raw) # Show raw response for debugging
        else:
            st.error("Failed to generate quiz. Please try again or check your API key.")
    else:
        st.warning("Please paste some content into the text area to generate a quiz.")

st.markdown("---") # Separator before quiz display

if st.session_state.quiz_generated and st.session_state.questions:
    st.subheader("Your Quiz:")
    for i, q_data in enumerate(st.session_state.questions):
        # Use a unique key for each radio button
        user_choice = st.radio(
            q_data["question"],
            q_data["options"],
            key=f"q{i}_radio",
            index=None # No pre-selected option
        )
        if user_choice:
            st.session_state.user_answers[i] = user_choice[0] # Store only the A/B/C/D part

    # Check Answers button
    if st.button("✅ Check Answers", use_container_width=True, type="secondary"):
        st.subheader("Quiz Results:")
        score = 0
        for i, q_data in enumerate(st.session_state.questions):
            user_ans_char = st.session_state.user_answers.get(i)
            correct_ans_char = q_data["correct_answer"]

            if user_ans_char:
                if user_ans_char == correct_ans_char:
                    st.success(f"Q{i+1}: Correct! ({q_data['question']})")
                    score += 1
                else:
                    st.error(f"Q{i+1}: Incorrect. Your answer: {user_ans_char}. Correct answer: {correct_ans_char}. ({q_data['question']})")
            else:
                st.warning(f"Q{i+1}: You didn't answer this question. Correct answer: {correct_ans_char}. ({q_data['question']})")
        st.markdown(f"### Your Score: {score} out of {len(st.session_state.questions)}")
        st.balloons() # Little celebratory animation for finishing the quiz
    else:
        st.info("Select your answers, then click 'Check Answers'.")
elif st.session_state.quiz_generated and not st.session_state.questions:
    st.error("No valid quiz questions could be generated. Please try again with different content.")