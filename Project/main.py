'''
Programmed by Sahand Sabet (https://github.com/SahandSbt)
Poll project with object oriented
Copy Righted by Apache License
'''

#-----------(Library)-----------

import os
import re
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
            print('\n ** ' , text[0] , ',' , text[1] , ',' , text[2] , end = '')
        print('')
    
    def re_ID(self):
        votes = []
        with open('votes.txt','r') as f:
            votes = f.readlines()
        for i in range(len(votes)):
            temp = votes[i].split(',')
            vote_str = str(i)
            for j in range(1,len(temp)):
                vote_str = vote_str + ',' + str(temp[j])
            votes[i] = vote_str
        with open('votes.txt','w') as f:
            for i in votes:
                f.write(i)

#-----------(Main User)-----------

class User:
    def __init__(self,email,password):
        self.email = email
        self.password = password
        self.participated_list = []
        self.created_list = []

    def recover(self):
        self.participated_list = []
        self.created_list = []
        try:
            with open(self.email + '.txt','r') as f:
                participated_list_temp = f.readline().split(',')
                created_list_temp = f.readline().split(',')
                for i in participated_list_temp:
                    if i != '' and i != '\n':
                        self.participated_list.append(i)
                for i in created_list_temp:
                    if i != '' and i != '\n':
                        self.created_list.append(i)
        except:
            with open(self.email + '.txt','w') as f:
                f.write('')
    
    def update_lists(self):
        participated_str = ''
        created_str = ''
        for i in range(len(self.participated_list)):
            participated_str = participated_str + self.participated_list[i] + ','
        for i in range(len(self.created_list)):
            created_str = created_str + self.created_list[i] + ','
        with open(self.email + '.txt','w') as f:
            f.write(participated_str + '\n' + created_str)


    def participate(self,ID,option):
        if str(ID) in self.participated_list:
            print("You participated before!")
            return
        self.participated_list.append(str(ID))
        with open('votes.txt','r') as f:
            ops = f.readlines()
            for i in range(len(ops)):
                info = ops[i].split(',')
                if info[0] == str(ID):
                    if info[1] == 'deactive':
                        print("Vote is deactive!")
                        return
                    ind = info.index(option)
                    info[ind+1] = int(info[ind+1]) + 1
                    txt = ''
                    for j in range(len(info)):
                        txt = txt + str(info[j])
                        if j != len(info) - 1:
                            txt += ','
                    if re.match(re.compile(r'^[0-9]+'),txt[-1:]):
                        txt += '\n'
                    ops[i] = txt
            with open('votes.txt','w') as fi:
                for i in ops:
                    fi.write(i)
        self.update_lists()

    def create(self,ID,title,options):
        self.created_list.append(str(ID))
        options_str = ''
        for i in options:
            options_str += ','
            options_str += str(i)
            options_str += ',0'
        add = str(ID) + ',active,' + title + options_str
        with open('votes.txt','a') as f:
            f.write(add + '\n')
        Poll.vote_list.append(add)
        self.update_lists()
    
    def delete(self,ID):
        if str(ID) not in self.created_list:
            print(" ** You didn't create this poll! ")
            return
        self.created_list.remove(str(ID))
        with open('votes.txt','r') as f:
            ops = f.readlines()
            for i in range(len(ops)):
                info = ops[i].split(',')
                if info[0] == str(ID):
                    ops[i] = 'temp'
            with open('votes.txt','w') as fi:
                for i in ops:
                    if 'temp' not in i:
                        fi.write(i)
        self.update_lists()
        
    def change_activation(self,ID):
        if str(ID) not in self.created_list:
            print(" ** You didn't create this poll! ")
            return
        with open('votes.txt','r') as f:
            ops = f.readlines()
            for i in range(len(ops)):
                info = ops[i].split(',')
                if info[0] == str(ID):
                    if info[1] == 'active':
                        info[1] = 'deactive'
                    else:
                        info[1] = 'active'
                    txt = ''
                    for j in range(len(info)):
                        txt = txt + str(info[j])
                        if j != len(info) - 1:
                            txt += ','
                    if re.match(re.compile(r'^[0-9]+'),txt[-1:]):
                        txt += '\n'
                    ops[i] = txt
            with open('votes.txt','w') as fi:
                for i in ops:
                    fi.write(i)
        self.update_lists()

#-----------(Admin)-----------     

class Admin(User):
    def __init__(self,email,password):
        super().__init__(email,password)
    
    def delete(self,ID):
        if str(ID) in self.created_list:
            self.created_list.remove(str(ID))
        with open('votes.txt','r') as f:
            ops = f.readlines()
            for i in range(len(ops)):
                info = ops[i].split(',')
                if info[0] == str(ID):
                    ops[i] = 'temp'
            with open('votes.txt','w') as fi:
                for i in ops:
                    if 'temp' not in i:
                        fi.write(i)
        self.update_lists()

#-----------(Authenticator)-----------

class Authenticator:
    def __init__(self, email, password):
        self.email = email
        md5_temp = hash.md5(str(password).encode('utf-8'))
        self.password = md5_temp.hexdigest()

    def authenticate(self, repeat_password, model):
        md5_temp = hash.md5(str(repeat_password).encode('utf-8'))
        repeat_password = md5_temp.hexdigest()
        email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not re.match(email_regex, self.email):
            print(" ** Wrong Email Syntax !")
            input("\n ** Press Enter To Reset **")
            exit()
        if model not in ['Admin','User'] or self.password != repeat_password:
            print(" ** Wrong Syntax !")
            input("\n ** Press Enter To Reset **")
            exit()

#-----------(Login)-----------

class Login:
    def __init__(self, email, password):
        self.email = email
        md5_temp = hash.md5(str(password).encode('utf-8'))
        self.password = md5_temp.hexdigest()

    def login(self):
        data = []
        with open('database.txt','r') as f:
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
        
        with open('database.txt','a') as f:
            text = str(self.email) + ',' + str(self.password) + ',' + model + '\n'
            f.write(text)
        return model

#-----------(CLI)----------- 

def CLI():
    print(" ** Welcome To Poll Project! **\n")
    print(" -- 1. Create a new poll\n -- 2. List of polls\n -- 3. Participate in a poll\n -- 4. Delete a poll\n -- 5. Change activation\n -- 6. Exit")
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
        user.create(ID_maker,title,options)
        print("\n ** Poll Successfully Created !")
        Poll.vote_recovery()

    elif choice == 2:
        Poll.print_list()

    elif choice == 3:
        ID = int(input("\n ** Enter the poll ID:\n => "))
        with open('votes.txt','r') as f:
            ops = f.readlines()
            for i in range(len(ops)):
                info = ops[i].split(',')
                if info[0] == str(ID):
                    for j in range(3,len(info),2):
                        print(' -> ' , info[j])
        vote = input("Enter your option: ")
        user.participate(ID,vote)
        print("\n ** Poll Successfully Voted !")
        user.recover()

    elif choice == 4:
        ID = int(input("\n ** Enter the poll ID:\n => "))
        user.delete(ID)
        Poll.re_ID()
        print("\n ** Poll Successfully deleted !")
        Poll.vote_recovery()

    elif choice == 5:
        ID = int(input("\n ** Enter the poll ID:\n => "))
        user.change_activation(ID)
        print("\n ** Poll Activation Successfully Changed !")
        Poll.vote_recovery()

    elif choice == 6:
        exit()

    else:
        print("\n ** Wrong Syntax !")
    input("\n ** Press Enter To Reset **")

#-----------(Main)----------- 

if __name__ == "__main__":
    Poll = PollInit()
    Poll.vote_recovery()
    status = input(" ** Enter your purpose (Register/Login): ")
    login_email = input(" ** Enter your email: ")
    login_password = input(" ** Enter your password: ")
    auth = None
    auth = Authenticator(login_email , login_password)
    log = Login(login_email , login_password)
    if status == 'Login':
        result = log.login()
    elif status == 'Register':
        reapeat_password = input(" ** Enter your password again: ")
        login_model = input(" ** Enter your character (Admin/User): ")
        auth.authenticate(reapeat_password, login_model)
        result = log.register(login_model)
    else:
        print("\n ** Wrong Syntax !")
        input("\n ** Press Enter To Reset **")
        exit()
    user = None
    print (result)
    if 'Admin' in result:
        user = Admin(login_email , login_password)
    elif 'User' in result:
        user = User(login_email , login_password)
    else:
        print(" ** Wrong email Or Password !")
        input("\n ** Press Enter To Exit **")
        exit()
    user.recover()
    os.system('cls' if os.name=='nt' else 'clear')
    while True:
        CLI()
        os.system('cls' if os.name=='nt' else 'clear')
