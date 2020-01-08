class Game:
    def __init__(self, id):
        self.p1endGuessing = False
        self.p2endGuessing = False
        self.p3endGuessing = False
        self.gameReady = False
        self.id = id
        self.points = [0, 0, 0]
        ##self.wins = [0,0,0]

    def get_player_points(self, p):
        return self.points[p]

    def play(self, player, points):
        self.points[player] = points
        if player == 0:
            self.p1endGuessing = True
        elif player == 1:
            self.p2endGuessing = True
        else:
            self.p3endGuessing = True
            
    def connected(self):
        return self.gameReady

    def allEndGuessing(self):
        return self.p1endGuessing and self.p2endGuessing and self.p3endGuessing

    def result(self):
        p1points = self.points[0]
        p2points = self.points[1]
        p3points = self.points[2]
        return p1points and p2points and p3points

    def resetGueassing(self):
        self.p1endGuessing = False
        self.p2endGuessing = False
        self.p3endGuessing = False