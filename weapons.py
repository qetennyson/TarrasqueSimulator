import random


class TwoHandedSword:
    def __init__(self, masterwork=False):
        self.damage = random.randint(1, 10)
        self.crit = 2.0
        self.masterwork = masterwork

    def __repr__(self):
        return 'Masterwork Two-Handed Sword'

class CompositeLongbow:
    def __init__(self, masterwork=False):
        self.damage = random.randint(1,8)
        self.crit = 3.0
        self.masterwork = masterwork

    def __repr__(self):
        return 'Masterwork Composite Longbow'