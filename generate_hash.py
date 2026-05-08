"""
Run this once to generate your ADMIN_PASSWORD_HASH for .env
Usage: python generate_hash.py
"""
import bcrypt
import getpass

password = getpass.getpass("Enter admin password: ")
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
print(f"\nADMIN_PASSWORD_HASH={hashed}")
