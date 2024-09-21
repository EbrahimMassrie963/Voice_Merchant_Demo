import os
import numpy as np
from dotenv import load_dotenv
import streamlit as st
from streamlit_mic_recorder import mic_recorder
from chatbot_function import OpenAIClient 
import tempfile
import io
from Ai import *
from get_data import info


    
# streamlit interface
with st.container():
    st.title("💬 TD Merchant Assistant Chatbot")
    
with st.container(height=600):
    messages = st.container()
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "system", "content": 
"Hello, I'm TD Merchant bot!", "avatar":"🤖"}]
    
    for msg in st.session_state.messages:
        messages.chat_message(msg["role"], 
avatar=msg["avatar"]).write(msg["content"])

with st.container():

    placeholder = st.empty()
    _, recording = placeholder.empty(), mic_recorder(
            start_prompt="START RECORDING YOUR QUESTION ⏺️", 
            stop_prompt="STOP ⏹️", 
            format="wav",
            use_container_width=True,
            key='recorder'
        )
    
    if recording:  
        service = st.session_state.get("service", None)
        if not service:
            prompt = """
              You Are a smart bot called 'TD bot'          
            Bot_Specific_Knowledge:
    ------ start of Bot_Specific_Knowledge ---------
    {info}
    ----------- end of Bot_Specific_Knowledge --------------------

    Respect these rules:
    ***most important rules**
    1. Always direct the user to the 'Treasure Deal' website when they ask you for anything outside of your information. Via the link 'https://demo.treasuredeal.com/'
    2. You cannot do actions. If the user asks you to do any action, ask him to visit the merchant page via the following link: 'https://www.google.com/'

    *** the rest of rules ***
    1. Don't justify your answers. Don't give information not mentioned in the Bot_Specific_Knowledge.
    2. Answer in the language the user asked you.
    3. Respond in a human-like, friendly, and polite manner, using a conversational tone.
    4. If the user tries to go off-topic, gently steer the conversation back to the Bot_Specific_Knowledge.
    5. Do not answer in a way that makes it obvious you are a bot. Ensure your responses sound natural and personable.
    6. Use a casual tone and speak as if you are talking to a friend, using informal language if appropriate.
    7. Include appropriate sentiments in your responses to make the conversation feel natural and engaging. Use emojis 😊👍 to convey emotions.
    8. Be interactive and use your communication skills to intelligently encourage the user to continue the conversation within Bot_Specific_Knowledge.
    9. Respond to the following query: user_input

            """.format(info = info)
            service = OpenAIClient(prompt)
            st.session_state.service = service
        audio_bio = io.BytesIO(recording['bytes'])  
        audio_bio.name = 'audio.mp3'
        user_question = service.speech_to_text_conversion(audio_bio)
        
        if user_question:
            bot_response = service.text_chat(user_question)
            st.session_state.messages.append({"role": "user", "content": 
user_question, "avatar":"👤"})
            
            st.session_state.messages.append({"role": "system", "content": 
bot_response, "avatar": "🤖"})
            
            if bot_response is not None:
                audio_data = service.text_to_speech_conversion(bot_response)  
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                    tmpfile.write(audio_data)
                    tmpfile_path = tmpfile.name
                    
                    # Play the audio automatically
                    placeholder.audio(tmpfile_path, format="audio/mp3", start_time=0,autoplay=True)
                        
