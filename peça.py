class Peça:

    def __init__(self, id, cor):
        self.id = id
        self.cor = cor

    def set_id(self, id):
        self.id = id

    def set_cor(self, cor):
        self.cor = cor

    def get_id(self):
        return self.id

    def get_cor(self):
        return self.cor
