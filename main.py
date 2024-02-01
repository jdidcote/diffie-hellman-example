from cipher import FernetCipher
from user import User
from utils import generate_prime_numbers

# Generate constants
p = generate_prime_numbers(100000)[-1]
g = 12

# Initialise users
user_1 = User(FernetCipher, g, p)
user_2 = User(FernetCipher, g, p)

# Share public keys
user_1.calculate_shared_secret(user_2.public_key)
user_2.calculate_shared_secret(user_1.public_key)

print("Publicly visible:")
print(f" - p: {p}\n - g: {g}")
print(f" - user_1 public key: {user_1.public_key}")
print(f" - user_2 public key: {user_2.public_key}")

user_1_message = user_1.encrypt_message("Secret message")
user_2_decoded_message = user_2.decrypt_message(user_1_message)

print(f"Decoded message using shared private key: {user_2_decoded_message}")
