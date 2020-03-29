import random
import time
from player import Play
from bot import Bot

global int_cards
overall_cards = []
bot_overall_cards = []
int_cards = []
check_counter = 0
deck_pot = 0
deck_raise = 0
starting_cash = 5000
#high_card[0] = ''
SPADES = ['2♤', '3♤', '4♤', '5♤', '6♤', '7♤', '8♤', '9♤', '10♤', 'J♤', 'Q♤', 'K♤', 'A♤']
CLUBS = ['2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣', 'A♣']
DIAMONDS = ['2♢', '3♢', '4♢', '5♢', '6♢', '7♢', '8♢', '9♢', '10♢', 'J♢', 'Q♢', 'K♢', 'A♢']
HEARTS = ['2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥', 'J♥', 'Q♥', 'K♥', 'A♥']

LIST_OF_CARDS = [SPADES, CLUBS, DIAMONDS, HEARTS]

CARD_RANKINGS = {
    'A': 13,
    'K': 12,
    'Q': 11,
    'J': 10,
    '10': 9,
    '9': 8,
    '8': 7,
    '7': 6,
    '6': 5,
    '5': 4,
    '4': 3,
    '3': 2,
    '2': 1
}
def ProbabilityCheck(cards):
    full_house_prob_pair = 0
    full_house_prob_three = 0
    y = False
    secondary_probability = 1
    probability = 0
    flush = []
    card_left_counter_r = 0
    card_left_counter_f = 0
    card_left_counter = 0
    iterator = 0
    remaining = 0
    flush_counter = 0
    int_counter = 0
    target_card = 0
    combined_list = []
    combined_list = [i for i in deck_cards]
    combined_list.extend([j for j in cards])
    y = False
    
    combined_list = list(dict.fromkeys(combined_list))
    for i in range(len(combined_list)):
        combined_list[i] = combined_list[i][:-1]
    x = False

    #royal flush
    count = 0
    spec_list = []
    prob_list = []
    new_list = []
    royal_flush_list = []
    flush_properties = list(dict.fromkeys([i[-1:] for i in cards]))
    flush_property = flush_properties[0]
    
    for i in LIST_OF_CARDS:
        for x in i:
            card_left_counter += 1

    if len(flush_properties) == 1:
        for i in LIST_OF_CARDS:
            for x in i:
                if flush_property in x:
                    spec_list.append(x)
                    for counter in range(len(spec_list)):
                        if counter > 7:
                            royal_flush_list.append(spec_list[counter])
        
        royal_flush_list = list(dict.fromkeys(royal_flush_list))
        
        prob_list.extend(cards)
        for i in prob_list:
            if i in royal_flush_list:
                count += 1
        counter = 0

        rem = 5 - count
        while rem > 0:
            counter += 1
            rem -= 1

    #flush
    cards = list(dict.fromkeys(cards))
    flush = [i[-1:] for i in cards]

    for i in flush:
        if flush.count(i) > flush_counter:
            flush_counter = flush.count(i)
            flush_type = i
    if flush_counter > 3:
        for i in LIST_OF_CARDS:
            for x in i:
                if flush_type in x:
                    spec_list = list(dict.fromkeys(spec_list))
                    spec_list.append(x)

        for i in cards:
            if i in spec_list:
                spec_list.remove(i)
        
        remaining = 5 - flush_counter

        if remaining > 1:
            while remaining > 0:
                secondary_probability *= (len(spec_list) - iterator) / (card_left_counter - iterator)
                iterator += 1
                remaining -= 1
        elif remaining == 1:
            secondary_probability = len(spec_list) / card_left_counter
        elif remaining == 0:
            secondary_probability = 1
        if probability != 1 and len(flush) != 7:
            if probability < secondary_probability:
                probability = secondary_probability

    #straight
    for i in range(len(int_cards) - 1):
        if int(int_cards[i + 1]) - int(int_cards[i]) == 1:
            new_list.append(int_cards[i]);new_list.append(int_cards[i + 1])
        else:
            if int(int_cards[i + 1]) - int(int_cards[i]) == 2:
                new_list.append(str(int(int_cards[i])))
                target_card = str(int(int_cards[i]) + 1)
    new_list = list(dict.fromkeys(new_list))

    if len(new_list) == 5:
        probability = 1

    elif len(new_list) == 4:
        #two tailed?
        if max(new_list) != '13' and min(new_list) != '2':
            counter = 0
            count = 0
            for x in LIST_OF_CARDS:
                for i in x:
                    if i[:-1] == str(int(new_list[-1]) + 1):
                        counter += 1
                    elif i[:-1] == str(int(new_list[0]) - 1):
                        count += 1
            secondary_probability = 0
            for i in range(len(new_list) - 1):#
                if int(new_list[i + 1]) - int(new_list[i]) == 1:
                    if probability < ((counter / card_left_counter) + (count / (card_left_counter - 1))):
                        probability = ((counter / card_left_counter) + (count / (card_left_counter - 1)))
                else:
                    break
        #head?
        if max(new_list) == '13':
            for i in LIST_OF_CARDS:
                for x in i:
                    if x[:-1] == '10':
                        target_card += 1
        #tail?
        elif min(new_list) == '1':
            for i in LIST_OF_CARDS:
                for x in i:
                    if x[:-1] == '6':
                        target_card += 1

    #four of a kind
    for x in combined_list:
        if combined_list.count(x) > 2:
            if combined_list.count(x) == 4:
                probability = 1
            else:
                if probability < 1 / card_left_counter:
                    probability = 1 / card_left_counter
                    y = True
        else:
            break

    #pair

    for x in combined_list:
        if combined_list.count(x) == 2:
            secondary_probability = 1
        else:
            secondary_probability = 0.2
            if probability < secondary_probability * 0.2:
                probability = secondary_probability * 0.2
        full_house_prob_pair = secondary_probability

    counter = 0
    count = 0
    secondary_probability = 0
    #three of a kind
    for x in combined_list:
        if combined_list.count(x) == 3:
            secondary_probability = 1
        elif combined_list.count(x) == 2:
            count += 1
            y = True
    count = count / 2
    if y:
        while count > 0:
            secondary_probability += 2 / (card_left_counter - counter) 
            counter += 1
            count -= 1
        full_house_prob_three = secondary_probability
        if probability < secondary_probability * 0.4:
            probability = secondary_probability * 0.4
    #full house
    if probability < full_house_prob_three * full_house_prob_pair:
        probability = full_house_prob_three * full_house_prob_pair * 0.65

    return probability

def Cash(starting_cash):
    with open('Poker.txt', 'w+') as f:
        f.write(f'{starting_cash}')

def Dealer():
    counter = 0
    player_cards = []
    while (counter < 2):

        random_number = random.randint(0, len(LIST_OF_CARDS) - 1)
        card_type = LIST_OF_CARDS[random_number]
        card_number = random.choice(card_type)
        player_cards.append(card_number)
        LIST_OF_CARDS[random_number].remove(card_number)
        counter += 1

    return player_cards

def Deck():
    counter = 0
    deck_cards = []

    while (counter < 3):

        random_number = random.randint(0, len(LIST_OF_CARDS) - 1)
        card_type = LIST_OF_CARDS[random_number]
        card_number = random.choice(card_type)
        deck_cards.append(card_number)
        LIST_OF_CARDS[random_number].remove(card_number)
        counter += 1

    return deck_cards

def Call(cash):
    global starting_cash
    global deck_pot
    starting_cash -= cash
    deck_pot += cash

def Check():
    return True

def Fold():
    return True

def Raise(raise_value):
    global starting_cash
    global deck_raise

    if raise_value < starting_cash:
        starting_cash -= raise_value
        deck_raise += raise_value
    else:
        pass

def Won():
    starting_cash += deck_pot

def DeckAdd(deck_cards):
    random_number = random.randint(0, len(LIST_OF_CARDS) - 1)
    card_type = LIST_OF_CARDS[random_number]
    card_number = random.choice(card_type)
    deck_cards.append(card_number)
    LIST_OF_CARDS[random_number].remove(card_number)

def PosComb(card):
    chance = 0
    straight_list = []
    straight_counter = 0
    int_cards = []
    highest_card = 0
    pair_counter = 0
    three_kind_counter = 0
    pair_list = []
    flush_count = 0
    three_list = []
    four_list = []
    straight_flush_flush = False
    straight_flush_straight = False
    full_house_pair = False
    full_house_three = False

    card = list(dict.fromkeys(card))
    combined_list = card
    print(card)
    for i in range(len(combined_list)):
        combined_list[i] = combined_list[i][:-1]
    #pairs
    for repeat in combined_list:
        pair_counter = combined_list.count(repeat)
        if pair_counter == 2:
            if pair_list.count(repeat) == 0:
                pair_list.append(repeat)
                full_house_pair = True
                chance = 0.2
        else:
            pair_counter = 0
            full_house_pair = False
    if len(pair_list) > 1:
        chance = 0.3
        
    #high card
    for i in card:

        try:
            if int_cards.count(CARD_RANKINGS[i]) == 0:
                int_cards.append(CARD_RANKINGS[i])
        except KeyError:
            continue
        if CARD_RANKINGS[i] > highest_card:
            highest_card = CARD_RANKINGS[i]
    int_cards.extend([CARD_RANKINGS[j[:-1]] for j in deck_cards if int_cards.count(CARD_RANKINGS[j[:-1]]) == 0])
    int_cards = list(dict.fromkeys(int_cards))

    high_card = [cards for cards, value in CARD_RANKINGS.items() if value == highest_card]

    if chance < 0.18:
        if high_card[0] == 'A' or high_card[0] == 'K' or high_card[0] == 'Q' or high_card[0] == 'J':
            if high_card[0] == 'A':
                chance = 0.18
            elif high_card[0] == 'K':
                chance = 0.17
            elif high_card[0] == 'Q':
                chance = 0.16
            elif high_card[0] == 'J':
                chance = 0.15


    #three of a kind
    for repeat in combined_list:
        three_kind_counter = combined_list.count(repeat)
        if three_kind_counter == 3:
            if three_list.count(repeat) == 0:
                three_list.append(repeat)
                chance = 0.4
                full_house_three = True
        else:
            three_kind_counter = 0
            full_house_three = False
    
    #four of a kind
    for repeat in combined_list:
        four_kind_counter = combined_list.count(repeat)
        if four_kind_counter == 4:
            if four_list.count(repeat) == 0:
                four_list.append(repeat)
                chance = 0.85
        else:
            four_kind_counter = 0

    #straight
    int_cards.sort()

    for i in range(0,len(int_cards) - 1):
        if i != len(int_cards) - 1:
            if int(int_cards[i + 1]) - int(int_cards[i]) != 1 and straight_counter < 4:
                straight_counter = 0
            else:
                straight_counter += 1
                straight_list.append(int_cards[i + 1]);straight_list.append(int_cards[i])
    straight_list.sort()
    straight_list = list(dict.fromkeys(straight_list))

    if straight_counter > 3:
        straight_flush_straight = True
        chance = 0.6
    else:
        straight_flush_straight = False

    #flush
    flush_list = [i for i in deck_cards]
    flush_list.extend([i for i in card])
    flush_list = list(dict.fromkeys(flush_list))
    flush_list = [i[-1:] for i in flush_list]

    for i in range(len(flush_list) - 1):
        flush_list[i] = flush_list[i][-1:]

    for element in flush_list:
        if flush_list.count(element) > 4:

            chance = 0.65
            straight_flush_flush = True
        else:
            straight_flush_flush = False

    #full house
    if full_house_pair == True and full_house_three == True:
        chance = 0.7
    
    #straight flush/royal flush
    if straight_flush_flush == True and straight_flush_straight == True:
        if straight_list[0] == 10:
            chance = 1
        else:
            chance = 0.95
    return chance

#game loop
while True:
    print('-------------\nWelcome to the Poker Casino\n-------------')
    print('Option 1: Start\n-\nOption 2: Starting Cash\n-\nOption 3: Quit\n')

    user_input = int(input())

    if user_input == 1:
        deck_cards = Deck()
        player = Play(Dealer())
        bot = Bot(Dealer())
        overall_cards.extend(player.cards)
        bot_overall_cards.extend(bot.cards)
        probability = 0
        while True:
            print(f'Cards in Hand: {player.cards}')
            Cash(starting_cash)
            answer = input('Call, Raise, Check or Fold: ')
            answer = answer.lower()
            if answer == 'call':
                print(deck_raise)
                if deck_raise != 0:
                    Call(deck_raise)
                else:
                    print('You cannot call 0$')

            elif answer == 'raise':
                raise_value = int(input('Raise Value: '))
                bot.BotMoves(probability, 'Raise')
                if raise_value > 0:
                    Raise(raise_value)

            elif answer == 'fold':
                bot.BotMoves(probability, 'Fold')
                break
            
            elif answer == 'check' and bot.BotMoves(probability, 'Check') == 'Check':
                check_counter += 1

                if check_counter > 1 and len(deck_cards) < 5:
                    DeckAdd(deck_cards)
                    #
                    overall_cards.extend(deck_cards)
                    #
                    bot_overall_cards.extend(deck_cards)

                print(f'Cards in Deck: {deck_cards}')
            if check_counter > 1:
                overall_cards = list(dict.fromkeys(overall_cards))
                bot.Probability(ProbabilityCheck(bot_overall_cards), PosComb(bot_overall_cards))
                player.Probability(PosComb(overall_cards))

            if check_counter == 3:
                if player.chance > bot.chance:
                    print('\n' * 100)
                    print('Player Wins!')
                    quit()
                elif player.chance < bot.chance:
                    print('\n' * 100)
                    print('Machine Wins!')
                    quit()
                else:
                    print('Draw')
                    quit()
                
    elif user_input == 2:
        print(f'You have {starting_cash}$')

    elif user_input == 3:
        break

    time.sleep(2)
