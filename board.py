import numpy as np
from player import Player
from termcolor import colored


class Board(object):
    
    def __init__(self,nb):
        self.grid = np.zeros((2,nb,nb),dtype=np.int8) #2 array nb*nb : one for the values and the other one for the player (1 or 2)
        self.player1 = Player(nb)   # real player
        self.AI = Player(nb) # AI
        self.player1.color = 'green'
        self.AI.color = 'blue'
        self.list_player = [self.player1,self.AI]
        self.user_first = True

    def display(self):

        print('\nHere is the game grid : \n')
        for i in range(self.grid[0].shape[0]):
            line = ''

            for j in range(self.grid[0].shape[1]):

                if self.grid[1,i,j]==1:
                    line += colored(str(self.grid[0,i,j]),self.player1.color)+" "
                elif self.grid[1,i,j]==2:
                    line += colored(str(self.grid[0,i,j]),self.AI.color)+" "
                elif self.grid[1,i,j]==-1:
                    line += colored('X','red')+" "
                else:
                    line += str(self.grid[0,i,j])+" "

            print(line)

        print('\n')
        
        print('Player set : ',colored(str(self.player1.chess),self.player1.color))
        print('AI set : ',colored(str(self.AI.chess),self.AI.color))
        print('\n')
    
    def play(self, row, column, weight, player):

        if weight in self.list_player[player-1].chess:
            if self.grid[1,row,column] == 0:

                self.grid[0,row,column] = weight
                self.grid[1,row,column] = player
                self.list_player[player-1].chess.remove(weight)
            else:
                print(colored('--Error please try again--','red'))
        
        else:
            print(colored('--Error please try again--','red'))
        

    def ask_player1(self):

        try:
            row_col_weight = input ("Enter row column and weight separated with spaces : ")
            row_col_weight = row_col_weight.split()
            row_col_weight = list(map(int, row_col_weight))
            self.play(row_col_weight[0],row_col_weight[1],row_col_weight[2],1)
        except:
            print(colored('--Error please try again--','red'))
            row_col_weight = input ("Enter row column and weight separated with spaces : ")
            row_col_weight = row_col_weight.split()
            row_col_weight = list(map(int, row_col_weight))
            self.play(row_col_weight[0],row_col_weight[1],row_col_weight[2],1)

    
    def extend_grid(self):

        padd_grid = np.zeros((self.grid[0].shape[0]+2,self.grid[0].shape[1]+2))
        padd_grid[1:-1,1:-1] = self.grid[0].copy()
        return padd_grid
    
    def round(self):

        self.display()
        
        if self.user_first:
            self.ask_player1()
            print('\n---AI playing---\n')
        else:
            print('\n---AI playing---\n')
            self.ask_player1()
        
        self.check()
        
    def start(self):

        # ask for leading
        leading = input ("User first ? (0/1): ")
        self.user_first = False if int(leading)==0 else True
        print('AI starts !') if int(leading)==0 else print('You start !')

        # while (len(self.player1.chess) >0) & (len(self.AI.chess) >0):
        while (len(self.player1.chess) >0):
            self.round()
        
        self.display()
        self.end_game()

        print(29*'-')
        print(10*'-'+'GAME OVER'+10*'-')
        print(29*'-')
        print('\n')
    
    def check(self):
        
        padd_grid = self.extend_grid()

        for i in range(self.grid[0].shape[0]):
            for j in range(self.grid[0].shape[1]):
                if np.sum(padd_grid[(i+1)-1:(i+1)+2,(j+1)-1:(j+1)+2]) >= 16 :
                    if self.grid[0,i,j] != 0 :
                        self.grid[1,i,j] = -1
                        self.grid[0,i,j] = 0

    def count_score(self,player):

        score = 0
        occurences =	{
            13: 0,
            8: 0,
            5: 0,
            3: 0,
            2: 0
            }

        for i in range(self.grid[1].shape[0]):
            for j in range(self.grid[1].shape[1]):
                if self.grid[1,i,j] == player:
                    score += self.grid[0,i,j]
                    occurences[self.grid[0,i,j]]+=1

        return score,occurences
    
    def end_game(self):
        
        # Winning and losing rules

        self.player1.score, self.player1.occurences = self.count_score(1)
        self.AI.score, self.AI.occurences = self.count_score(2)
        
        print('User score = '+self.player1.score+' and '+'AI score = '+self.AI.score)

        if self.player1.score == self.AI.score:
            for chess in [13, 8, 5, 3, 2]:
                if self.player1.occurences[chess] > self.AI.occurences[chess]:
                    print('\nYou won against AI, congrats !\n')
                    return 0
                elif self.player1.occurences[chess] < self.AI.occurences[chess]:
                    print('\nAI won, try again to beat my AI !\n')
                    return 0
        elif self.player1.score > self.AI.score:
            print('\nYou won against AI, congrats !\n')
            return 0
        else:
            print('\nAI won, try again to beat my AI !\n')
            return 0