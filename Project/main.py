'''
Programmed by Sahand Sabet (https://github.com/SahandSbt)
Poll project with object oriented
Copy Righted by Apache License
'''

#-----------(Library)-----------

import os
import hashlib as hash

#-----------(Poll_Init)-----------

class PollInit:
    def __init__(self):
        self.vote_list = []

    def vote_recovery(self): 
        with open('votes.txt','r') as f:
            self.vote_list = f.readlines()

    def print_list(self):
        for i in self.vote_list:
            text = i.split(',')
            print('\n ** ' , text[0] , ',' , text[1] , end = '')
        print('')

#-----------(Main User)-----------

class User:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.user_list = []

    def recover(self):
        try:
            with open(self.username + '.txt','r') as f:
                self.user_list = f.readlines()
        except:
            with open(self.username + '.txt','w') as f:
                f.write('')

#-----------(Participator)-----------

class Participator(User):
    def __init__(self,username,password):
        super().__init__(username,password)
    
    def participate(self,ID,option):
        for i in range(len(user.user_list)):
            if str(ID) in user.user_list[i-1]:
                print("You participated before!")
                return
        with open(self.username + '.txt','a') as f:
            f.write(str(ID) + '\n')
        with open('votes.txt','r') as f:
            ops = f.readlines()
            for i in range(len(ops)):
                info = ops[i].split(',')
                if info[0] == str(ID):
                    ind = info.index(option)
                    info[ind+1] = int(info[ind+1]) + 1
                    txt = ''
                    for j in range(len(info)):
                        txt = txt + str(info[j])
                        if j != len(info) - 1:
                            txt += ','
                    ops[i] = txt
            with open('votes.txt','w') as fi:
                for i in ops:
                    fi.write(i)
    
#-----------(Admin)-----------     

class Admin(User):
    def __init__(self,username,password):
        super().__init__(username,password)

    def create(self,ID,title,options):
        options_str = ''
        for i in options:
            options_str += ','
            options_str += str(i)
            options_str += ',0'
        add = str(ID) + ',' + title + options_str
        with open('votes.txt','a') as f:
            f.write(add + '\n')
        Poll.vote_list.append(add)

#-----------(Login)-----------

class Login:
    def __init__(self, username, password):
        self.username = username
        md5 = hash.md5(str(password).encode('utf-8'))
        self.password = md5.hexdigest()

    def login(self):
        data = []
        with open('database.txt','r') as f:
            data = f.readlines()
        for i in data:
            person = i.split(',')
            if person[0] == self.username:
                if person[1] == self.password:
                    return person[2]
                else:
                    return "deny"
        return "deny"
    
    def register(self,model):
        if model not in ['Admin','Participator']:
            print(" ** Wrong Syntax !")
            input("\n ** Press Enter To Reset **")
            exit()
        with open('database.txt','a') as f:
            text = str(self.username) + ',' + str(self.password) + ',' + model + '\n'
            f.write(text)
        return model

#-----------(CLI)----------- 

def CLI():
    print(" ** Welcome To Poll Project! **\n")
    print(" -- 1. Create a new poll\n -- 2. List of polls\n -- 3. Participate in a poll\n -- 4. Exit")
    choice = int(input(" => "))

    if choice == 1:
        title = input("\n ** Enter the poll title:\n => ")
        number = int(input("\n ** Enter the option counts:\n => "))
        options = []
        ID_maker = 0
        for i in range(number):
            option = input(" ** Option " + str(i+1) + " : ")
            options.append(option)
        with open('votes.txt','r') as f:
            temp = f.readlines()
            ID_maker = len(temp)
        try:
            user.create(ID_maker,title,options)
            print("\n ** Poll Successfully Created !")
            Poll.vote_recovery()
        except:
            print(" ** Participators can't make a poll !")

    elif choice == 2:
        Poll.print_list()

    elif choice == 3:
        ID = int(input("\n ** Enter the poll ID:\n => "))
        with open('votes.txt','r') as f:
            ops = f.readlines()
            for i in range(len(ops)):
                info = ops[i].split(',')
                if info[0] == str(ID):
                    for j in range(2,len(info),2):
                        print(' -> ' , info[j])
        vote = input("Enter your option: ")
        try:
            user.participate(ID,vote)
            print("\n ** Poll Successfully Voted !")
            user.recover()
        except:
            print(" ** Admins can't participate !")

    elif choice == 4:
        exit()

    else:
        print("\n ** Wrong Syntax !")
    input("\n ** Press Enter To Reset **")

#-----------(Main)----------- 

if __name__ == "__main__":
    Poll = PollInit()
    Poll.vote_recovery()
    status = input(" ** Enter your purpose (Register/Login): ")
    login_username = input(" ** Enter your username: ")
    login_password = input(" ** Enter your password: ")
    log = None
    log = Login(login_username , login_password)
    if status == 'Login':
        result = log.login()
    elif status == 'Register':
        login_model = input(" ** Enter your character (Admin/Participator): ")
        result = log.register(login_model)
    else:
        print("\n ** Wrong Syntax !")
        input("\n ** Press Enter To Reset **")
        exit()
    user = None
    print('>'+result)
    if 'Admin' in result:
        user = Admin(login_username , login_password)
    elif 'Participator' in result:
        user = Participator(login_username , login_password)
    else:
        print(" ** Wrong Username Or Password !")
        input("\n ** Press Enter To Exit **")
        exit()
    user.recover()
    os.system('cls' if os.name=='nt' else 'clear')
    while True:
        CLI()
        os.system('cls' if os.name=='nt' else 'clear')
