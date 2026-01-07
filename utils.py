import os
from openai import OpenAI

def call_gpt(prompt, model="gpt-3.5-turbo", api_key=None):
    """
    Calls the OpenAI GPT API with a given prompt and model.

    Args:
        prompt (str): The input prompt for the GPT model.
        model (str): The GPT model to use (default: "gpt-3.5-turbo").
        api_key (str): The OpenAI API key. If not provided, the client will
                       attempt to use the OPENAI_API_KEY environment variable.

    Returns:
        str: The generated content from the GPT model, or None if an error occurs.
    """
    # Use environment variable if no key provided
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OpenAI API key is not set.")
        return "Error: OpenAI API key not configured."
    
    # Initialize the OpenAI client with the API key
    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None