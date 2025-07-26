class sharedData:
    x: int
    results: dict
    pe: int

    def __init__(self):
        self.x = 0
        self.results = "IBM"
        self.pe = 25

    def setX(self, x_value: int):
        self.x = x_value

    def getX(self):
        return self.x
    
    def set_list(self, value: dict):
        self.results = value

    def get_list(self):
        return self.results
    
    def set_pe(self, value: int):
        self.pe = value
    
    def get_pe(self):
        return self.pe
    

shared = sharedData()