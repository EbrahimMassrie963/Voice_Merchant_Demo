import requests
import json

def caesar_encrypt(text, shift):
    """
    Encrypt the given text using Caesar cipher with the specified shift.
    """
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
    """
    Decrypt the given text using Caesar cipher with the specified shift.
    """
    return caesar_encrypt(text, -shift)
class APIClientWithDynamicSystem:
    """
    Class to handle responses from a chat completion API with a default system message
    that can be updated dynamically.
    """

    def __init__(self, url, api_key, model, system_message="You are a helpful assistant."):
        """
        Initialize the APIClient with the API URL, API key, model, and a default system message.

        Args:
            url (str): The API endpoint URL.
            api_key (str): The API key for authorization.
            model (str): The model to be used for generating completions.
            system_message (str): The default system message to guide the assistant's behavior.
        """
        self.url = url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        self.model = model
        self.system_message = {"role": "system", "content": system_message}

    def change_system_message(self, new_system_message):
        """
        Change the default system message.

        Args:
            new_system_message (str): The new system message to guide the assistant's behavior.
        """
        self.system_message = {"role": "system", "content": new_system_message}

    def get_content(self, messages):
        """
        Get content from the API based on the provided message sequence, adding the current system message.

        Args:
            messages (list): A list of messages (without a system message).

        Returns:
            str: The content received from the API.
        """
        # Prepend the system message if not already provided
        full_messages = [self.system_message] + messages

        data = {
            "model": self.model,
            "messages": full_messages
        }

        response = requests.post(self.url, headers=self.headers, json=data)
        
        if response.status_code == 200:
            try:
                json_data = response.json()
                content = json_data.get("choices", [])[0].get("message", {}).get("content", "")
                return content
            except (json.JSONDecodeError, IndexError):
                return "Error parsing response."
        else:
            return f"API request failed with status code {response.status_code}."
