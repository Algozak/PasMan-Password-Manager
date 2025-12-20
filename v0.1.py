import json
import time
import sys
import os
from getpass import getpass
base_name = "basepass.json"
users_base = "users_base.json"

def show_banner():
    time.sleep(0.5)
    print("\n========================================\n\033[34m        P   A   S   M   A   N\033[0m\n\033[33m   Your Personal Password Manager\033[0m\n========================================\n")
    auto_reg()
def auto_reg():
    print("\033[32m---Добро пожаловать---\033[0m\n")
    time.sleep(0.5)
    return auto_menu()
def auto_menu():
    try:
        reg_input = int(input("\n1. Войти\n2. Регистрация\nВыберите пункт (1/2) >>> "))
        if reg_input == 1:
            request()
        elif reg_input == 2:
            time.sleep(1)
            register()
            time.sleep(1)
            request()
        else:
            print("\n\n\033[31m---Ошибка---\033[0m")
            time.sleep(0.5)
            print("\033[31m---Такого пункта нет---\033[0m")
            return auto_menu()  
    except ValueError:
        print("\n\033[31m---Ошибка---\033[0m")
        time.sleep(0.5)
        print("\033[31m---Такого пункта нет---\033[0m\n")
        return auto_menu()        
#register
def register_login():
    with open(users_base,'r',encoding='utf-8') as checkfile:
        global user_login
        user_login = input("\nПридумайте имя пользователя: ")
        if len(user_login) > 16:
            print("\033[33m---Слишком длинное имя--- (Макс.кол символов 16)\033[0m")
            time.sleep(1)
            return register_login()
        elif len(user_login) < 4:
            print("\033[33m---Слишком короткое имя--- (Мин.кол символов 4)\033[0m")
            time.sleep(1)
            return register_login()
        else:
            checklogin()      
def checklogin():
    if not os.path.exists(users_base):
        return False
    with open(users_base, 'r', encoding='utf-8') as file:
        data = json.load(file)
    if any(user['login'] == user_login for user in data):
        print("Имя пользователя занято")
        return register_login()
    else:
        return register_password()
def register_password():
    global user_password
    user_password = input("Придумайте пароль: ")    
    if len(user_password) > 16:
        print("\033[33m---Слишком длинный пароль--- (Макс.кол символов 16)\033[0m")
        time.sleep(1)
        return register_password()
    elif len(user_password) < 4:
        print("\033[33m---Слишком короткий пароль--- (Мин.кол символов 4)\033[0m")
        time.sleep(1)
        return register_password()
    else:
        print("\033[32m\n---Хорошо---\033[0m\n")  
        save_user(users_base,user_data={"login":user_login,"password":user_password}) 
def save_user(users_base, user_data):
    if not os.path.exists(users_base):
        initial_data = [user_data]  
        with open(users_base, 'w', encoding='utf-8') as file:
            json.dump(initial_data, file, ensure_ascii=False, indent=2)
    else:
        with open(users_base, 'r', encoding='utf-8') as file1:
            existing_data = json.load(file1)
        if not isinstance(existing_data, list):
            existing_data = [existing_data]
        existing_data.append(user_data)
        with open(users_base, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=2)
    print("\033[32m---Вы успешно зарегистрировались---\033[0m\n")
    return request()
def register():
    register_login()
    register_password()
    
#singin
def sign_login():
    login_input = input("Имя пользователя: ")
    
def sign_password():
    password_input = getpass('Пароль: ')
def signin():
    sign_login()
    sign_password()

def request():
    try:
        user_choose = int(input("\n1. Записать новый пароль\n2. Посмотреть пароль\n3. Удалить запись\n4. Показать список сервисов\n5. Выход\nВыберите пункт >>> "))
        if user_choose == 1:
            service()
        elif user_choose == 5:
            end()
    except ValueError:
        print("----ОШИБКА!----")
        time.sleep(1)
        print("----Такой пункт не найден----")
        time.sleep(1)
        print("----Можете выбрать снова----\n\n")
        time.sleep(1)
        return request() 

def service():
    with open(base_name,"r",encoding="utf-8") as base:
        global data
        try: 
            data = json.load(base)
        except json.JSONDecodeError:
            data = {"example":"example"}    
        global service_input
        service_input = input("Название сервиса >>> ")
        if len(service_input) < 4:
            print("\n---Ошибка---")
            time.sleep(1)
            print("---Мин.кол символов 4---\n")
            return service()
        elif len(service_input) > 16:
            print("\n---Ошибка---")
            time.sleep(1)
            print("---Макс.кол символов 16---\n")
            return service()
        else:
            global value
            for key,value in data.items():
                if service_input == key:
                    print("Подождите...")
                    time.sleep(2)
                    print("---Сервис найден---")
                    time.sleep(1)
                    rewrite()
                else:
                    add_service()     

def rewrite():
        try:
            value_input = int(input("1.Перезаписать пароль\n2.Отмена\n\n >>> "))
            if value_input == 1:
                user_pass = input("Введите старый пароль: ")
                if user_pass == value["password"]:
                    time.sleep(1)
                    print("---Пароли совподают---")
                    time.sleep(1)
                    new_user_pass = input("Введите новый пароль (Макс.кол символов 16): ")
                    if len(new_user_pass) > 16:
                        print("---ОШИБКА---")
                        time.sleep(1)
                        print("---Слишком длинный пароль---")
                        return rewrite()
                    elif len(new_user_pass) < 8:
                        print("---ОШИБКА---")
                        time.sleep(1)
                        print("---Мин.кол.символов 8---")
                        return rewrite()
                    else:
                        time.sleep(1)
                        data[str(service_input)]['password'] = new_user_pass
                        with open(base_name,'w',encoding='utf-8') as file:
                            json.dump(data,file,ensure_ascii=False, indent=2)
                            print("---Новый пароль сохранен---") 
                            return service()    
                else:
                    print("---Ошибка---")
                    time.sleep(0.5)
                    print("---Пароли не совподают---")
                    return service()
            elif value_input == 2:
                return request()
            else:
                print("---Ошибка---\n ")
                return value_input   
        except ValueError or UnboundLocalError:
            print("Ошибка :(")
            return value_input

def add_service_login():
        print(f"\nНазвание сервиса - <<{service_input}>>")
        login_input = input("Придумайте Login: ")
        if len(login_input) > 16:
            print("\n---Ошибка---")
            time.sleep(1)
            print("---Макс.кол символов 16---")
            return add_service_login()
        elif len(login_input) < 4:
            print("\n---Ошибка---")
            time.sleep(1)
            print("---Мин.кол символов 4---")
            return add_service_login()        
def add_service_password():
    global password_input
    password_input = input("Придумайте Пароль: ")
    if len(password_input) > 16:
        print("\n---Ошибка---")
        time.sleep(1)
        print("---Макс.кол символов 16---\n")
        return add_service_password()
    elif len(password_input) < 6:
        print("\n---Ошибка---")
        time.sleep(1)
        print("---Мин.кол символов 8---\n")
        return add_service_password()


#1
def add_service():
    add_service_login()
    add_service_password()                                                          
#2
def see_pass():
    pass
#3
def del_pass():
    pass
#4
def show():
    pass
#5
def end():
    print('Завершение работы ...')
    time.sleep(1)
    sys.exit(0)


if __name__ == "__main__":
    show_banner()