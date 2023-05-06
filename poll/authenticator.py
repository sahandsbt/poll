import hashlib as hash
import re

class Authenticator:
    def __init__(self, email, password):
        self.email = email
        md5_temp = hash.md5(str(password).encode('utf-8'))
        self.password = md5_temp.hexdigest()

    def authenticate(self, repeat_password, model):
        md5_temp = hash.md5(str(repeat_password).encode('utf-8'))
        repeat_password = md5_temp.hexdigest()
        email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        password_regex = re.compile(r'[a-zA-Z]+')
        if not re.match(email_regex, self.email) or not re.match(password_regex, self.password):
            print(" ** Wrong Email / Password Syntax! **")
            input("\n ** Press Enter To Reset **")
            exit()
        if model not in ['Admin','User'] or self.password != repeat_password:
            print(" ** Wrong Syntax! **")
            input("\n ** Press Enter To Reset **")
            exit()

class Login:
    def __init__(self, email, password):
        self.email = email
        md5_temp = hash.md5(str(password).encode('utf-8'))
        self.password = md5_temp.hexdigest()

    def login(self):
        data = []
        with open('data/database.txt','r') as f:
            data = f.readlines()
        for i in data:
            person = i.split(',')
            if person[0] == self.email:
                if person[1] == self.password:
                    return person[2]
                else:
                    return "deny"
        return "deny"
    
    def register(self, model):
        
        with open('data/database.txt','a') as f:
            text = str(self.email) + ',' + str(self.password) + ',' + model + '\n'
            f.write(text)
        return model