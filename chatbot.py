import ollama

def get_bot_response(user_input: str, model_name: str = "llama3.2:latest") -> str:

    if not user_input.strip():
        return "Please enter a message."

    try:
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": user_input.strip()}]
        )
        bot_reply = response["message"]["content"]
        return bot_reply
    except Exception as e:
        return f"Error calling model: {e}"


