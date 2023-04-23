import os

class PollInit:
    def __init__(self):
        self.vote_list = []

    def vote_recovery(self):  
        try:             
            with open('data/votes.txt','r') as f:
                self.vote_list = f.readlines()
        except:
            try:
                os.makedirs('data')
            except:
                pass
            with open('data/votes.txt','x') as f:
                pass
    def print_list(self):
        for i in self.vote_list:
            text = i.split(',')
            print('\n ** ' , text[0] , ',' , text[1] , ',' , text[2] , end = '')
        print('')

    def re_ID(self):
        votes = []
        with open('data/votes.txt','r') as f:
            votes = f.readlines()
        for i in range(len(votes)):
            temp = votes[i].split(',')
            vote_str = str(i)
            for j in range(1,len(temp)):
                vote_str = vote_str + ',' + str(temp[j])
            votes[i] = vote_str
        with open('data/votes.txt','w') as f:
            for i in votes:
                f.write(i)