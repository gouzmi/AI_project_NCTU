class Player(object):

    def __init__(self,nb):
        
        if(nb==4):
            self.chess = [2,3,5,8,13]
        elif(nb==6):
            self.chess = [2,2,3,3,5,5,8,8,8,13,13]
        else:
            print(str(nb),'is not playable')
        