import streamlit as st
from gemini_streaming import GeminiChatbot

def main():
    st.set_page_config(
        page_title="MG's Chatbot",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("MG's AI Chatbot")
    st.markdown("Chat with Google's Gemini model")
    
    # Initialize chatbot in session state if not already present
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = GeminiChatbot()
        
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Load initial conversation history (skip system message)
        for message in st.session_state.chatbot.conversation_history[1:]:
            st.session_state.messages.append({
                "role": message["role"],
                "content": message["content"]
            })
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What would you like to ask?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.chatbot.add_message("user", prompt)
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            assistant_response = ""
            
            # Get streaming response
            response = st.session_state.chatbot.client.chat.completions.create(
                messages=st.session_state.chatbot.conversation_history,
                model=st.session_state.chatbot.model_name,
                stream=True
            )
            
            for update in response:
                if update.choices and update.choices[0].delta:
                    content = update.choices[0].delta.content or ""
                    assistant_response += content
                    response_placeholder.markdown(assistant_response)
            
            # Add assistant response to session state and chatbot history
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            st.session_state.chatbot.add_message("assistant", assistant_response)

    # Add a clear button
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.chatbot = GeminiChatbot()
        st.rerun()

if __name__ == "__main__":
    main()