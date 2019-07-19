class Peca():
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return "[{}|{}]" .format(self.first, self.second)

    def __contains__(self, key):
        return key == self.first or key == self.second

    def __del__(self):
        del self  

    def invert(self):
        self.first, self.second = self.second, self.first

    def is_startable(self):
        return self.first == 6 and self.second == 6
    
    def is_removable(self):
        return self.first == 0 and self.second == 0
