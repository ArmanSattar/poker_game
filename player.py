class Play():
    def __init__(self, cards):
        self.cards = cards
        print(f'Player Deck: {self.cards}')

    def Probability(self, chance):
        self.chance = chance
        print(f'Player Chance: {chance}')