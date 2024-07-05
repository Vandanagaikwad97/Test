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
    tweaks=TWEAKS,
    api_key="sk-zMgHX6Dmos8GLD6Gy-zUBOMqnKDy49Rl0tWChFNiOlc"  # Add this if you have an API key
    )  
    st.write("Debug - Raw response:", response)

        assistant_response = "I'm sorry, I couldn't generate a response."
        if isinstance(response, dict):
            if "detail" in response:
                st.error(f"API Error: {response['detail']}")
            elif 'outputs' in response:
                # ... (your existing parsing logic)
            else:
                st.warning("Unexpected response format from API")
        else:
            st.warning("Response is not a dictionary as expected")

    except requests.exceptions.RequestException as e:
        st.error(f"Error making request to Langflow API: {str(e)}")
    except json.JSONDecodeError:
        st.error("Error decoding JSON from API response")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
