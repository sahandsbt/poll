class UserInterface:
    def __init__(self, Poll_obj, User):
        self.Poll_obj = Poll_obj
        self.User = User
    
    def CLI(self):
        print(" ** Welcome To Poll Project! **\n")
        print(" -- 1. Create a new poll\n -- 2. List of polls\n -- 3. Participate in a poll\n -- 4. Delete a poll\n -- 5. Change activation\n -- 6. My polls\n -- 7. Exit")
        choice = int(input(" => "))

        if choice == 1:
            title = input("\n ** Enter the poll title:\n => ")
            number = int(input("\n ** Enter the option counts:\n => "))
            options = []
            ID_maker = 0
            for i in range(number):
                option = input(" ** Option " + str(i+1) + " : ")
                options.append(option)
            with open('data/votes.txt','r') as f:
                temp = f.readlines()
            try:
                ID_maker = temp[len(temp)-1].split(',')
                ID_maker = int(ID_maker[0]) + 1
            except:
                ID_maker = 0
            self.User.create(self.Poll_obj,ID_maker,title,options)
            self.Poll_obj.vote_recovery()

        elif choice == 2:
            self.Poll_obj.print_list()

        elif choice == 3:
            ID = int(input("\n ** Enter the poll ID:\n => "))
            with open('data/votes.txt','r') as f:
                ops = f.readlines()
                for i in range(len(ops)):
                    info = ops[i].split(',')
                    if info[0] == str(ID):
                        for j in range(3,len(info),2):
                            print(' -> ' , info[j])
            vote = input(" ** Enter your option: ")
            self.User.participate(ID,vote)
            self.User.recover()

        elif choice == 4:
            ID = int(input("\n ** Enter the poll ID:\n => "))
            self.User.delete(ID)
            self.Poll_obj.vote_recovery()

        elif choice == 5:
            ID = int(input("\n ** Enter the poll ID:\n => "))
            self.User.change_activation(ID)
            self.Poll_obj.vote_recovery()

        elif choice == 6:
            my_polls_str = ''
            for i in range(len(self.User.created_list)):
                my_polls_str += ' '
                my_polls_str += self.User.created_list[i]
                if i != len(self.User.created_list)-1:
                    my_polls_str += ','
            print(" ** Your poll ID's :" + my_polls_str + " **")
            
        elif choice == 7:
            exit()

        else:
            print("\n ** Wrong Syntax! **")
            
        input("\n ** Press Enter To Reset **")