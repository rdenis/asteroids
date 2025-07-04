class Player:
    def __init__(self, position, health):
        self.position = position
        self.health = health

    def move(self, new_position):
        self.position = new_position

    def attack(self):
        # Implement attack logic here
        pass


class Enemy:
    def __init__(self, position, strength):
        self.position = position
        self.strength = strength

    def move(self, new_position):
        self.position = new_position

    def attack(self):
        # Implement attack logic here
        pass