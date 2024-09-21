import os
import datetime
from dotenv import load_dotenv
from openai import OpenAI
def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():  # Check if the character is a letter
            shift_base = ord('a') if char.islower() else ord('A')
            encrypted_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
            encrypted_text += encrypted_char
        else:
            encrypted_text += char  # Non-alphabetic characters remain unchanged
    return encrypted_text

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

load_dotenv()
api_key=os.getenv("API_KEY")
api_key=caesar_decrypt(api_key, 3)
class OpenAIClient:
    def __init__(self,prompt):
        openai_api_key =api_key  # Get the API key from the .env file
        self.client = OpenAI(api_key=openai_api_key)
        self.messages=[
                {"role": "system", "content": prompt}
            ]
        

    def speech_to_text_conversion(self, audio_file):
        """Converts audio format message to text using OpenAI's Whisper model."""
        transcription = self.client.audio.transcriptions.create(
                model="whisper-1",  # Model to use for transcription
                file=audio_file  # Audio file to transcribe
            )
        return transcription.text

    def text_chat(self, text):
        """Generate a response using OpenAI based on the context provided."""
        self.messages.append({"role": "user", "content": text})
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages)
        bot=response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": bot})
        return bot

    def text_to_speech_conversion(self, text):
        """Converts text to audio format message using OpenAI's text-to-speech model - tts-1."""
        if text:
            speech_file_path = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_speech.webm"
            response = self.client.audio.speech.create(
                model="tts-1-hd",  # Model to use for text-to-speech conversion
                # voices types: alloy, echo, fable, onyx, nova, and shimmer
                voice="nova",  # Voice to use for speech synthesis
                input=text  # Text to convert to speech
            )
            response.stream_to_file(speech_file_path)  # Streaming synthesized speech to file
            # Read the audio file as binary data
            with open(speech_file_path, "rb") as audio_file:
                audio_data = audio_file.read()
            os.remove(speech_file_path)
            return audio_data
