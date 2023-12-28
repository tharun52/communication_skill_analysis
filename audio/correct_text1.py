import openai

# Set your OpenAI API key
openai.api_key = 'api-key'

def correct_grammar(original_text):
    # Construct a prompt for the GPT model
    prompt = f"Improve the following text:\n{original_text}\n\nImproved text:"

    try:
        # Make a request to the OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300  # Adjust as needed
        )

        # Extract and return the generated text
        improved_text = response['choices'][0]['text']
        return improved_text

    except openai.error.RateLimitError as e:
        # Handle RateLimitError (exceeded quota)
        print(f"Rate limit exceeded. Error: {e}")
        return "Sorry, the service is currently unavailable. Please try again later."

    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
        return "An error occurred while processing the text."
