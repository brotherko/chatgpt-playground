import time
from os import environ

from .singleton import Singleton

from pychatgpt.classes import openai as OpenAI
from pychatgpt.classes import chat as Chat
from pychatgpt.classes import spinner as Spinner
from pychatgpt.classes import exceptions as Exceptions

import colorama
from colorama import Fore

class ChatHandler(Singleton):
    def __init__(self):
        self.email=environ.get('OPENAI_EMAIL')
        self.password=environ.get("OPENAI_PASSWORD")
        self.proxies=environ.get("OPENAI_PROXY")

        self.__auth_access_token: str or None = None
        self.__auth_access_token_expiry: int or None = None

        self._setup()

    def _setup(self):
        if self.proxies is not None:
            if not isinstance(self.proxies, dict):
                if not isinstance(self.proxies, str):
                    raise Exceptions.PyChatGPTException("Proxies must be a string or dictionary.")
                else:
                    self.proxies = {"http": self.proxies, "https": self.proxies}

        # Check for access_token & access_token_expiry in env
        if OpenAI.token_expired():
            print(f"{Fore.RED}>> Access Token missing or expired."
                  f" {Fore.GREEN}Attempting to create them...")
            self._create_access_token()
        else:
            access_token, expiry = OpenAI.get_access_token()
            self.__auth_access_token = access_token
            self.__auth_access_token_expiry = expiry

            try:
                self.__auth_access_token_expiry = int(self.__auth_access_token_expiry)
            except ValueError:
                print(f"{Fore.RED}>> Expiry is not an integer.")
                raise Exceptions.PyChatGPTException("Expiry is not an integer.")

            if self.__auth_access_token_expiry < time.time():
                print(f"{Fore.RED}>> Your access token is expired. {Fore.GREEN}Attempting to recreate it...")
                self._create_access_token()

    def _create_access_token(self) -> bool:
        openai_auth = OpenAI.Auth(email_address=self.email, password=self.password, proxy=self.proxies)
        openai_auth.create_token()

        # If after creating the token, it's still expired, then something went wrong.
        is_still_expired = OpenAI.token_expired()
        if is_still_expired:
            print(f"{Fore.RED}>> Failed to create access token.")
            return False

        # If created, then return True
        return True
    
    def healthcheck(self):
        try:
            self.ask("hello!", None, None)
            return True
        except:
            return False

    def ask(self, prompt: str, conversation_id: str, previous_convo_id: str) -> str or None:
        if prompt is None:
            print(f"{Fore.RED}>> Enter a prompt.")
            raise Exceptions.PyChatGPTException("Enter a prompt.")

        if not isinstance(prompt, str):
            raise Exceptions.PyChatGPTException("Prompt must be a string.")

        if len(prompt) == 0:
            raise Exceptions.PyChatGPTException("Prompt cannot be empty.")

        # Check if the access token is expired
        if OpenAI.token_expired():
            print(f"{Fore.RED}>> Your access token is expired. {Fore.GREEN}Attempting to recreate it...")
            did_create = self._create_access_token()
            if did_create:
                print(f"{Fore.GREEN}>> Successfully recreated access token.")
            else:
                print(f"{Fore.RED}>> Failed to recreate access token.")
                raise Exceptions.PyChatGPTException("Failed to recreate access token.")

        # Get access token
        access_token = OpenAI.get_access_token()
        response = Chat.ask(auth_token=access_token,
                                                           prompt=prompt,
                                                           conversation_id=conversation_id,
                                                           previous_convo_id=previous_convo_id,
                                                           proxies=self.proxies)
        
        answer, conversation_id, previous_convo_id = response
                                                        
        if answer == "400" or answer == "401":
            print(f"{Fore.RED}>> Failed to get a response from the API.")
            return None
        
        print(f"answer = {answer}")

        return response