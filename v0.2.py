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
        with open(self.filename,'w') as f:
            json.dump(data,f,indent=4,ensure_ascii=False)        
            
            
class PasswordManagerApp:
    def __init__(self):
        self.ui = AppInterface("PasMan","Your Personal Password Manager",'0.2','Добро Пожаловать')
        self.is_running = True

    def run(self):
        self.ui.show_banner()

        if self.is_running:
            self.ui.main_menu()
            


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
        print(f'{' '*6}{'-'*5} {self.welcome} {'-'*5}')

    def main_menu(self):
        print("\n1. Add Password\n2. Get Password\n3. Show a list of services\n4. Delete the password\n5. Exit")
        choice = input("Select option: ")
            
        if choice == "1":
            svc = input("Service: ")
            pwd = input("Password: ")
            self.storage.add(svc, pwd)
            time.sleep(0.5)
            print(f"\n{'-'*4}Тhe password is saved{'-'*4}")
        elif choice == "2":
            svc_input = input("Service name >>> ")
            self.storage.get_password(svc_input)
        elif choice == '3':
            self.storage.svc_list()
        elif choice == '4':
            del_input = input("Which service's password do you want to delete?\n >>> ")
            self.storage.del_password(del_input)    
        elif choice == "5":
            time.sleep(0.5)
            self.is_running = False
            print(f"\nGoodbye!\n")
            time.sleep(0.5)


if __name__ == "__main__":
    app = PasswordManagerApp()
    app.run()
