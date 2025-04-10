import os
from openai import OpenAI

class GeminiChatbot:
    def __init__(self):
        self.token = os.environ["GOOGLE_API_KEY"]
        self.endpoint = "https://generativelanguage.googleapis.com/v1beta/openai/"
        self.model_name = "gemini-2.0-flash"
        
        self.client = OpenAI(
            base_url=self.endpoint,
            api_key=self.token,
        )
        
        # Initialize conversation history
        self.conversation_history = [
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            }
        ]
    
    def add_message(self, role, content):
        """Add a message to the conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content,
        })
    
    def get_response(self):
        """Get a streaming response from the model."""
        response = self.client.chat.completions.create(
            messages=self.conversation_history,
            model=self.model_name,
            stream=True,
            stream_options={'include_usage': True}
        )
        
        assistant_response = ""
        usage = None
        
        for update in response:
            if update.choices and update.choices[0].delta:
                content = update.choices[0].delta.content or ""
                print(content, end="")
                assistant_response += content
            if update.usage:
                usage = update.usage
        
        # Add the complete assistant response to conversation history
        self.add_message("assistant", assistant_response)
        
        if usage:
            print("\n")
            for k, v in vars(usage).items():
                print(f"{k} = {v}")
    
    def run(self):
        """Run the chatbot in a loop."""
        print("Gemini Chatbot initialized. Type 'exit' to quit.")
        
        while True:
            # Prompt the user for input
            user_input = input("\nEnter your question or prompt (or type 'exit' to quit): ")
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            
            # Add user input and get response
            self.add_message("user", user_input)
            self.get_response()


if __name__ == "__main__":
    chatbot = GeminiChatbot()
    chatbot.run()