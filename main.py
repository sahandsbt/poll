'''
Programmed by Sahand Sabet (https://github.com/SahandSbt)
Poll project with object oriented
Copy Righted by Apache License
'''

import poll.authenticator as authenticator
import poll.initiator as initiator
import poll.processor as processor
import poll.interface as interface
import os

def main():
    Poll = initiator.PollInit()
    Poll.vote_recovery()
    status = input(" ** Enter your purpose (Register/Login): ")
    login_email = input(" ** Enter your email: ").lower()
    login_password = input(" ** Enter your password: ")
    auth = None
    auth = authenticator.Authenticator(login_email , login_password)
    log = authenticator.Login(login_email , login_password)
    if status == 'Login':
        result = log.login()
    elif status == 'Register':
        reapeat_password = input(" ** Enter your password again: ")
        login_model = 'User' # Changable (Admin/User)
        auth.authenticate(reapeat_password, login_model)
        result = log.register(login_model)
    else:
        print("\n ** Wrong Syntax! **")
        input("\n ** Press Enter To Reset **")
        exit()
    if 'Admin' in result:
        user = processor.Admin(login_email , login_password)
    elif 'User' in result:
        user = processor.User(login_email , login_password)
    else:
        print(" ** Wrong email Or Password! **")
        input("\n ** Press Enter To Exit **")
        exit()
    user.recover()
    os.system('cls' if os.name=='nt' else 'clear')
    while True:
        cli = interface.UserInterface(Poll,user)
        cli.CLI()
        os.system('cls' if os.name=='nt' else 'clear')

if __name__ == "__main__":  
    main()
