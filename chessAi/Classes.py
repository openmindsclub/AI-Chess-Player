class Movebranche():
    def __init__(self):
        self.moves = []

    def addmove(self, move):
        self.moves.append(move)

    def branche_value(self, value):
        self.value = value

    def pop(self):
        self.moves.pop()
