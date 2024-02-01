from abc import ABC, abstractmethod

from cryptography.fernet import Fernet


class BaseCipher(ABC):
    def __init__(self, key: bytes) -> None:
        self.key = key

    @abstractmethod
    def encrypt(self, message: str) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, message: str) -> bytes:
        pass


class FernetCipher(BaseCipher):
    def __init__(self, key: bytes) -> None:
        super().__init__(key)
        self.fernet = Fernet(key)

    def encrypt(self, message: str) -> bytes:
        return self.fernet.encrypt(message.encode())

    def decrypt(self, encrypted_message: bytes) -> str:
        return self.fernet.decrypt(encrypted_message).decode()
