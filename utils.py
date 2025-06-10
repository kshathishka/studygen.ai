import openai
import streamlit as st

openai.api_key = st.secrets["openai"]["api_key"]

def call_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()
