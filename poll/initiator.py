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
        