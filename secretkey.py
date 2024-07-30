import secrets
import os

# Generate a secure random string with 32 bytes (256 bits)
secret_key = secrets.token_hex(32)

print("Secure Secret Key:", secret_key)
