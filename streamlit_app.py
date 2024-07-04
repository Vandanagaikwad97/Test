import streamlit as st
from langflow_api import run_flow, FLOW_ID, TWEAKS
import json

st.title("Langflow Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is your question?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from Langflow
    response = run_flow(
        message=prompt,
        endpoint=FLOW_ID,
        output_type="chat",
        input_type="chat",
        tweaks=TWEAKS
    )

    assistant_response = "I'm sorry, I couldn't generate a response."
    if isinstance(response, dict) and 'outputs' in response:
        outputs = response['outputs']
        if outputs and isinstance(outputs[0], dict) and 'outputs' in outputs[0]:
            inner_outputs = outputs[0]['outputs']
            if inner_outputs and isinstance(inner_outputs[0], dict) and 'results' in inner_outputs[0]:
                results = inner_outputs[0]['results']
                if 'result' in results:
                    assistant_response = results['result']

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
