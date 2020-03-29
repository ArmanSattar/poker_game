import random

class Bot:
    def __init__(self, cards):
        self.cards = cards

    def Probability(self, probability, chance):
        self.probability = probability
        self.chance = chance
        print(f'Bot chance: {chance}')

    def BotMoves(self, probability, command):
        x = random.randint(1,10)
        try:
            if self.probability == None:
                self.probability = probability
        except AttributeError:
            self.probability = 0
            self.chance = 0
        print(f'Bluff: {x} ; {probability}')

        #bluff move
        if command == 'Check' or command == 'Raise':
            if x < 4:
                print('Raise')
                return 'Raise'
            
            elif self.probability < 0.1 and self.chance < 0.5:
                print('Check')
                return 'Check'
            
            else:
                print('Raise')
                return 'Raise'
        
        if command == 'Raise':
            if self.probability == 1 and self.chance > 0.4:
                print('All in')
                return 'All in'
            
            elif (self.probability > 0.1 and self.chance > 0.5) and (self.probability < 0.18 and self.chance < 0.7):
                print('Raise')
                return 'Raise'
            
            elif self.probability > 0.18 and self.chance > 0.8:
                print('All in')
                return 'All in'

        elif self.probability < 0.05 and self.chance < 0.2:
            print('Fold')
            return 'Fold'
