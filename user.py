import base64
import os
import random
from typing import Type

from cipher import BaseCipher
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from utils import is_prime


class User:
    _global_salt = os.urandom(16)

    def __init__(self, cipher_class: Type[BaseCipher], g: int, p: int, max_private_value: int = 1e6) -> None:
        if not is_prime(p):
            raise ValueError("p must be a prime number")

        if g >= p:
            raise ValueError("g must be greater than p")

        self.g = g
        self.p = p
        self._private_key = random.randint(1, max_private_value)
        self.public_key = self._generate_public_key()
        self._shared_secret = None
        self._cipher_class = cipher_class
        self._cipher = None

    def _generate_public_key(self) -> int:
        return pow(self.g, self._private_key, self.p)

    def calculate_shared_secret(self, other_public_key: int) -> None:
        shared_secret_integer = pow(other_public_key, self._private_key, self.p)
        self._shared_secret = shared_secret_integer
        self._initialise_cipher(self._cipher_class)

    def _derive_key(self) -> bytes:
        if not self._shared_secret:
            raise ValueError("No stored shared secret.")

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self._global_salt,
            iterations=100000,
            backend=default_backend(),
        )
        key = kdf.derive(str(self._shared_secret).encode())
        return base64.urlsafe_b64encode(key)

    def _initialise_cipher(self, cipher_class: Type[BaseCipher]) -> None:
        key = self._derive_key()
        self._cipher = cipher_class(key)

    def encrypt_message(self, message: str) -> str:
        return self._cipher.encrypt(message)

    def decrypt_message(self, encrypted_message: str) -> str:
        return self._cipher.decrypt(encrypted_message)


