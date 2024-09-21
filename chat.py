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
    def __init__(self, prompt):
        self.client = OpenAI(api_key=api_key)
        self.messages = [
            {"role": "system", "content": prompt}
        ]

    def text_chat(self, text):
        """Generate a response using OpenAI based on the context provided."""
        self.messages.append({"role": "user", "content": text})
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages)
        bot=response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": bot})
        return bot
    


