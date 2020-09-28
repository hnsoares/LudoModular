class Casa:

    def __init__(self, id, cor, is_specil):
        self.id = id
        self.cor = cor
        self.is_special = is_special

    def set_id(self, id):
        self.id = id

    def set_cor(self, cor):
        self.cor = cor

    def set_is_special(self, is_special):
        self.is_special = is_special

    def get_id(self):
        return self.id

    def get_cor(self):
        return self.cor

    def get_is_special(self):
        return self.is_special
