# OOP Version
import time
import json
import os
import hashlib
import os

class CredentialManager:
    def __init__(self, filename="vault.json"):
        self.filename = filename
        self.__vault = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return {}

    def add(self, service, password):
        self.__vault[service] = password
        with open(self.filename, "w") as f:
            json.dump(self.__vault, f, indent=4)

    def get_password(self,service):
        if service in self.__vault:
            print(f'\nPassword : {self.__vault[service]}') 
        else:
            print("Not found")
    def svc_list(self):
        with open(self.filename,'r') as file:
            data = json.load(file)
            svclist = list(data)
            for index,service in enumerate(svclist,start=1):
                print(f'\n{'='*20}')
                print(f'{index}.{service}')
    def del_password(self,service):
        with open(self.filename,'r') as file:
            data = json.load(file)
            if service in data:
                del data[service]
                print(f'Тhe service was successfully deleted')
            else:
                time.sleep(0.5)
                print(f"\n{'-'*4}Service not found{'-'*4}\n")    
        with open(self.filename,'w') as f:
            json.dump(data,f,indent=4,ensure_ascii=False)        
            

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
        self.ui = AppInterface("PasMan","Your Personal Password Manager",'0.2','Welcome')
        
        self.is_running = True

    def run(self):
        auth = AuthManager()
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
                time.sleep(0.5)
                self.ui.main_menu()
                return
            else:
                attempts -= 1
                print(f"Wrong! Left: {attempts}")
    
        print("Locked out.")


class AppInterface:
    def __init__(self,name,description,version,welcome):
        self.storage = CredentialManager()
        self.name = name
        self.description = description
        self.version = version
        self.welcome = welcome
        

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
            self.storage.add(svc, pwd)
            time.sleep(0.5)
            print(f"\n{'-'*4}Тhe password is saved{'-'*4}")
            time.sleep(2)
            return self.main_menu()
        elif choice == "2":
            svc_input = input("Service name >>> ")
            self.storage.get_password(svc_input)
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
