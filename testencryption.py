from cryptography.fernet import Fernet
import os

log_dir = "/Users/mannatvirk/.hiddenfolder"
key_file = os.path.join(log_dir, "encryption_key.key")

print(f"log_dir: {log_dir}")


if os.path.exists(key_file):
    with open(key_file, "rb") as f:
        key = f.read()
else:
    print("Encryption key not found. Exiting.")
    exit()

cipher = Fernet(key)

def encrypt_file(filepath):
    try:
        if os.path.exists(filepath):
            print(f"Encrypting {filepath}...")
            with open(filepath, "rb") as f:
                file_data = f.read()
            encrypted_data = cipher.encrypt(file_data)
            with open(filepath, "wb") as f:
                f.write(encrypted_data)
            print(f"Encryption of {filepath} completed.")
        else:
            print(f"File {filepath} does not exist.")
    except Exception as e:
        print(f"Error encrypting {filepath}: {e}")

test_file_path = os.path.join(log_dir, "test.txt")
with open(test_file_path, "w") as f:
    f.write("This is a test for encryption.")

encrypt_file(test_file_path)
print("Check if test.txt has been encrypted.")
