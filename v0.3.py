# OOP Version
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import time
import json
import os
import hashlib
import os
from cryptography.fernet import Fernet
class CredentialManager:
    def __init__(self, filename="vault.json"):
        self.filename = filename
        self.__check = self.check_file_exists()
        self._vault = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return {}

    def check_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename,'w') as f:
                return json.dump({},f)

    def add(self, service, password):
        self._vault[service] = password
        with open(self.filename, "w") as f:
            json.dump(self._vault, f, indent=4)

    def svc_list(self):
        with open(self.filename,'r') as file:
            data = json.load(file)
            if not data:
                print(f'\n{'-'*4}Список Пуст{'-'*4}\n')
            else:    
                svclist = list(sorted(data))
                for index,service in enumerate(svclist,start=1):
                    print(f'\n{'='*20}')
                    print(f'{index}.{service}')
    def del_password(self,service):
        with open(self.filename,'r') as file:
            data = json.load(file)
            if service in data:
                del self._vault[service]
                with open(self.filename,'w') as f:
                    json.dump(self._vault,f,indent=4,ensure_ascii=False) 
                print(f'Тhe service was successfully deleted')    
            else:
                time.sleep(0.5)
                print(f"\n{'-'*4}Service not found{'-'*4}\n")    
               


class PasswordCrypto:
    def __init__(self,master_password):
        self.salt = b'some_salt_'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(master_password.encode())
        b64_key = base64.urlsafe_b64encode(key)
        self.cipher_suite = Fernet(b64_key)
    
    def encrypt(self,plain_text):
        return self.cipher_suite.encrypt(plain_text.encode())
    def decrypt(self,cipher_text):
        return self.cipher_suite.decrypt(cipher_text).decode()        


class AuthManager:
    def __init__(self, auth_file="shadow.bin"):
        self.auth_file = auth_file
        self.is_authenticated = False

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_first_run(self):
        return not os.path.exists(self.auth_file)

    def setup_master(self, password):
        with open(self.auth_file, "w") as f:
            f.write(self._hash_password(password))
        print("Master password set!")

    def verify(self, input_password):
        if not os.path.exists(self.auth_file):
            return False
        
        with open(self.auth_file, "r") as f:
            stored_hash = f.read()
        
        if self._hash_password(input_password) == stored_hash:
            self.is_authenticated = True
            return True
        return False


class PasswordManagerApp:
    def __init__(self):
        self.ui = AppInterface("PasMan","Your Personal Password Manager",'0.2','Welcome',None)
        self.is_running = True

    def run(self):
        auth = AuthManager()
        self.storage = CredentialManager()
        self.ui.show_banner()
        if auth.check_first_run():
            new_pass = input("Create your Master Password: ")
            auth.setup_master(new_pass)
    
        attempts = 3
        while attempts > 0:
            entered_pass = input("Enter Master Password: ")
            if auth.verify(entered_pass):
                time.sleep(0.5)
                print(f"\n{'-'*5}Access Granted!{'-'*5}")
                self.storage.check_file_exists()
                crypto_tool = PasswordCrypto(entered_pass)
                app = AppInterface("PasMan","Your Personal Password Manager",'0.2','Welcome',crypto_tool)
                time.sleep(0.5)
                app.main_menu()
                return
            else:
                attempts -= 1
                print(f"Wrong! Left: {attempts}")
    
        print("Locked out.")


class AppInterface:
    def __init__(self,name,description,version,welcome,crypto):
        self.storage = CredentialManager()
        self.name = name
        self.description = description
        self.version = version
        self.welcome = welcome
        self.crypto = crypto

    def show_banner(self):
        print('=' * 40)
        print(f'{' '*12}{self.name}{' '*4}v{self.version}\n{' '*6}{self.description}')
        print('=' * 40)
        time.sleep(1)
        print(f'\n{' '*6}{'-'*5} {self.welcome} {'-'*5}\n\n')

    def main_menu(self):
        print("\n1. Add Password\n2. Get Password\n3. Show a list of services\n4. Delete the password\n5. Exit")
        choice = input("Select option: ")
            
        if choice == "1":
            svc = input("Service: ")
            pwd = input("Password: ")
            encrypted_pwd = self.crypto.encrypt(pwd)
            self.storage.add(svc, encrypted_pwd.decode())
            time.sleep(0.5)
            print(f"\n{'-'*4}Тhe password is saved{'-'*4}")
            time.sleep(2)
            return self.main_menu()
        elif choice == "2":
            svc_input = input("Service name >>> ")
            if svc_input in self.storage._vault:
                decrypted_password = self.crypto.decrypt(self.storage._vault[svc_input].encode())
                print(f'\nPassword : {decrypted_password}')
            else:
             print("Not found")    
            time.sleep(2)
            return self.main_menu()
        elif choice == '3':
            self.storage.svc_list()
            time.sleep(2)
            return self.main_menu()
        elif choice == '4':
            del_input = input("Which service's password do you want to delete?\n >>> ")
            self.storage.del_password(del_input)
            time.sleep(2)
            return self.main_menu()    
        elif choice == "5":
            time.sleep(0.5)
            self.is_running = False
            print(f"\nGoodbye!\n")
            time.sleep(0.5)


if __name__ == "__main__":
    app = PasswordManagerApp()
    app.run()
