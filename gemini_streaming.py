import os
from openai import OpenAI

token = os.environ["GOOGLE_API_KEY"]
endpoint = "https://generativelanguage.googleapis.com/v1beta/openai/"
model_name = "gemini-2.0-flash"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

# Initialize conversation history
conversation_history = [
    {
        "role": "system",
        "content": "You are a helpful assistant.",
    }
]

while True:
    # Prompt the user for input
    user_input = input("Enter your question or prompt (or type 'exit' to quit): ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # Add user input to the conversation history
    conversation_history.append({
        "role": "user",
        "content": user_input,
    })

    # Get the response from the model
    response = client.chat.completions.create(
        messages=conversation_history,
        model=model_name,
        stream=True,
        stream_options={'include_usage': True}
    )

    usage = None
    for update in response:
        if update.choices and update.choices[0].delta:
            print(update.choices[0].delta.content or "", end="")
            # Add the assistant's response to the conversation history
            conversation_history.append({
                "role": "assistant",
                "content": update.choices[0].delta.content or "",
            })
        if update.usage:
            usage = update.usage

    if usage:
        print("\n")
        for k, v in vars(usage).items():  # Replaced usage.dict() with vars(usage)
            print(f"{k} = {v}")