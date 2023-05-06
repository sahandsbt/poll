import re

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
            with open('data/' + self.email + '.txt','r') as f:
                participated_list_temp = f.readline().split(',')
                created_list_temp = f.readline().split(',')
                for i in participated_list_temp:
                    if i != '' and i != '\n':
                        self.participated_list.append(i)
                for i in created_list_temp:
                    if i != '' and i != '\n':
                        self.created_list.append(i)
        except:
            with open('data/' + self.email + '.txt','w') as f:
                f.write('')
    
    def update_lists(self):
        participated_str = ''
        created_str = ''
        for i in range(len(self.participated_list)):
            participated_str = participated_str + self.participated_list[i] + ','
        for i in range(len(self.created_list)):
            created_str = created_str + self.created_list[i] + ','
        with open('data/' + self.email + '.txt','w') as f:
            f.write(participated_str + '\n' + created_str)


    def participate(self,ID,option):
        if str(ID) in self.participated_list:
            print(" ** You participated before! **")
            return
        self.participated_list.append(str(ID))
        with open('data/votes.txt','r') as f:
            ops = f.readlines()
            for i in range(len(ops)):
                info = ops[i].split(',')
                if info[0] == str(ID):
                    if info[1] == 'deactive':
                        print(" ** Vote is deactive! **")
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
            with open('data/votes.txt','w') as fi:
                for i in ops:
                    fi.write(i)
        self.update_lists()
        print("\n ** Poll Successfully Voted! **")

    def create(self,Poll_obj,ID,title,options):
        self.created_list.append(str(ID))
        options_str = ''
        for i in options:
            options_str += ','
            options_str += str(i)
            options_str += ',0'
        add = str(ID) + ',active,' + title + options_str
        with open('data/votes.txt','a') as f:
            f.write(add + '\n')
        Poll_obj.vote_list.append(add)
        self.update_lists()
        print("\n ** Poll Successfully Created! **")
    
    def delete(self,ID):
        if str(ID) not in self.created_list:
            print(" ** You didn't create this poll! **")
            return
        self.created_list.remove(str(ID))
        with open('data/votes.txt','r') as f:
            ops = f.readlines()
            for i in range(len(ops)):
                info = ops[i].split(',')
                if info[0] == str(ID):
                    ops[i] = 'temp'
            with open('data/votes.txt','w') as fi:
                for i in ops:
                    if 'temp' not in i:
                        fi.write(i)
        self.update_lists()
        print("\n ** Poll Successfully deleted! **")
        
    def change_activation(self,ID):
        if str(ID) not in self.created_list:
            print(" ** You didn't create this poll! **")
            return
        with open('data/votes.txt','r') as f:
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
            with open('data/votes.txt','w') as fi:
                for i in ops:
                    fi.write(i)
        self.update_lists()
        print("\n ** Poll Activation Successfully Changed! **")

class Admin(User):
    def __init__(self,email,password):
        super().__init__(email,password)
    
    def delete(self,ID):
        if str(ID) in self.created_list:
            self.created_list.remove(str(ID))
        with open('data/votes.txt','r') as f:
            ops = f.readlines()
            for i in range(len(ops)):
                info = ops[i].split(',')
                if info[0] == str(ID):
                    ops[i] = 'temp'
            with open('data/votes.txt','w') as fi:
                for i in ops:
                    if 'temp' not in i:
                        fi.write(i)
        self.update_lists()
        print("\n ** Poll Successfully deleted! **")
