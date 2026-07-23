PasMan - Secure Password Manager (v0.3.1)

PasMan is a console-based password manager written in Python, built on OOP principles and providing a high level of security for your local data.

PasMan stores data and protects it reliably:

    AES Encryption: All passwords are encrypted using the cryptography library (Fernet). Even if someone steals your JSON file, they'll only see a meaningless set of characters.

    PBKDF2 Key Derivation: The encryption key isn't stored in the code — it's generated on the fly from your Master Password.

    Input Validation: "Foolproof" protection. Checks password length, composition, and the correctness of service names.

    Colorized UI: An updated interface with ANSI colors and smooth delays (time.sleep) for a better user experience.

Core Features

    Add Password: Save a service with automatic complexity checking.

    Get Password: Instant decryption and password output.

    Show Services: A convenient list of all resources.

    Delete Entry: Secure deletion of entries.

    Master Auth: System login via hashed password (SHA-256).

 Technologies

    Language: Python 3.10+

    Security: cryptography (Fernet), hashlib (SHA-256).

    Storage: Encrypted JSON.

    OS: Optimized for Linux (Fedora/Ubuntu).

Installation and Setup

--- Clone the repository:
```bash
git clone https://github.com/Algozak/PasMan-Password-Manager.git
cd PasMan-Password-Manager
```
---Install dependencies:
```bash
pip install cryptography
```
--- Run the current version:
```bash
python pasman.py
```
