from ..model import bdd 

class User():

    def __init__(self, id):
        self.user_info = bdd.get_user_info(id)

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.user_info["id"])

