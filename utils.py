from openai import OpenAI

def call_gpt(prompt, model="gpt-3.5-turbo", api_key="AIzaSyC3AmOc6m24u3KoIuRlG4qgHihz9I0pLjA"):
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
    # Check if an API key is provided directly to the function
    # If not, it will fall back to checking the OPENAI_API_KEY environment variable
    # when the OpenAI client is initialized without an explicit api_key argument.
    # However, to avoid an error if neither is set, we'll initialize the client
    # with the provided api_key, which can be an empty string.
    if not api_key:
        print("Warning: OpenAI API key is not provided. The client will attempt to use "
              "the 'OPENAI_API_KEY' environment variable. If neither is set, "
              "API calls will likely fail.")
        # Initialize client without an explicit api_key, letting it
        # attempt to load from environment variables.
        client = OpenAI()
    else:
        # Initialize the OpenAI client with the provided API key
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