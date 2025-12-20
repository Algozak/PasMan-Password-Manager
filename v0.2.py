# OOP Version
import time
import json
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
class PasswordManagerApp:
    def __init__(self):
        self.ui = AppInterface("PasMan","Your Personal Password Manager",'0.2','Добро Пожаловать')
        self.storage = CredentialManager()
        self.is_running = True

    def run(self):
        self.ui.show_banner()

        while self.is_running:
            print("\n1. Add Password\n2. Get Password\n3. Exit")
            choice = input("Select option: ")
            
            if choice == "1":
                svc = input("Service: ")
                pwd = input("Password: ")
                self.storage.add(svc, pwd)
            elif choice == "2":
                svc_input = input("Service name >>> ")
                self.storage.get_password(svc_input)
            elif choice == "3":
                self.is_running = False
                print("Goodbye!")                                      
class AppInterface:
    def __init__(self,name,description,version,welcome):
        self.name = name
        self.description = description
        self.version = version
        self.welcome = welcome
        

    def show_banner(self):
        print('=' * 40)
        print(f'{' '*12}{self.name}{' '*4}v{self.version}\n{' '*6}{self.description}')
        print('=' * 40)
        time.sleep(1)
        print(f'{' '*6}{'-'*5} {self.welcome} {'-'*5}')

if __name__ == "__main__":
    app = PasswordManagerApp()
    app.run()
