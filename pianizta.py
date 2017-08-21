import time
import random

total_cards:   int = 36
player_cards:  int = 18
similar_cards: int = 4
cards:        dict = {0: 'six', 1: 'seven', 2: 'eight', 3: 'nine', 4: 'ten', 5: 'jack', 6: 'queen', 7: 'king', 8: 'ace'}

# global accessed data
p1_deck:      list = []
p2_deck:      list = []
card_buffer:  list = []  # buffer for current action, no more than 2 card objects should be within this buffer
stack_buffer: list = []  # buffer for similar card pull outs situation
deck_values:  list = [0x0, 0x1]
turns = 0


def generate_cards():
    generated_cards: list = []
    item_counter:     int = 0

    for card_value in cards:
        while item_counter != 4:
            generated_cards.append([card_value, cards.get(card_value), item_counter])
            item_counter += 1
        item_counter = 0
    return generated_cards


def shuffle_cards(card_set):
    allocated_cards: dict = {}
    n: int = 0
    for item in card_set:
        allocated_cards.update({n: item})
        n += 1

    random.shuffle(allocated_cards)
    return allocated_cards


def deal_cards(card_set):
    global p1_deck, p2_deck
    p1_deck = []
    p2_deck = []
    x: int = 0

    for card in card_set.items():
        if x % 2:
            p1_deck.append(card)
        else:
            p2_deck.append(card)
        x += 1


def handle_cards():
    global card_buffer

    winner:        int = 0x0
    final_handle: bool = False
    # 0x0 value for player 1 winner
    # 0x1 value for player 2 winner
    while not final_handle:
        if check_len():
            break
            
        if card_buffer[0][1][0] == card_buffer[1][1][0]:
            handle_similar_cards()
            final_handle = True
        
        else:
            if card_buffer[0][1][0] is 8 and card_buffer[1][1][0] is 0:
                winner += 1
                final_handle = True

            elif card_buffer[0][1][0] is 0 and card_buffer[1][1][0] is 8:
                final_handle = True

            elif card_buffer[0][1][0] > card_buffer[1][1][0]:
                final_handle = True

            elif card_buffer[0][1][0] < card_buffer[1][1][0]:
                winner += 0x1
                final_handle = True

            if final_handle:
                push_player_deck(winner)
                break

    return [True, winner]  # if handle was successful


def push_player_deck(deck_value):
    # pushes cards from card buffer into given deck
    global p1_deck, p2_deck, deck_values, card_buffer

    if deck_value == deck_values[0]:
        for card in card_buffer:
            p1_deck.append(card)
    else:
        for card in card_buffer:
            p2_deck.append(card)

    card_buffer = []


def pull_player_deck(deck_value):
    # pulls card from given deck into card buffer
    global p1_deck, p2_deck, deck_values, card_buffer

    try:
        if deck_value == deck_values[0]:
            card_buffer.extend(p1_deck[0:1]), p1_deck.pop(0)
        else:
            card_buffer.extend(p2_deck[0:1]), p2_deck.pop(0)
    except IndexError:
        pass


def handle_similar_cards():
    global p1_deck, p2_deck, stack_buffer, card_buffer, deck_values

    transfer_to_stack()
    pull_player_deck(0x0), pull_player_deck(0x1)
    transfer_to_stack()
    pull_player_deck(0x0), pull_player_deck(0x1)
    challenge = handle_cards()

    if challenge[0]:
        for card_set in reversed(stack_buffer):
            for card in card_set:
                if challenge[1] == deck_values[0]:
                    p1_deck.append(card)
                else:
                    p2_deck.append(card)

        stack_buffer = []


def transfer_to_stack():
    global card_buffer, stack_buffer

    stack_buffer.append(card_buffer)
    card_buffer = []


def dump_held_cards(do_p=False, title='default debug title'):
    print(title + '\n')
    if do_p:
        print('player 1')
        print(len(p1_deck))
        for item in p1_deck:
            print('\t' + str(item))
        print('player 2')
        print(len(p2_deck))
        for item in p2_deck:
            print('\t' + str(item))

    print('card buffer')
    print(len(card_buffer))
    for item in card_buffer:
        print('\t' + str(item))

    print('stack buffer')
    print(len(stack_buffer))
    for item in stack_buffer:
        print('\t' + str(item))


def check_len():
    global p1_deck, p2_deck

    if len(p1_deck) == 0 or len(p2_deck) == 0:
        return True
    else:
        return False


def smart_pull(i):
    if i % 2:
        pull_player_deck(0x0)
        pull_player_deck(0x1)
    else:
        pull_player_deck(0x1)
        pull_player_deck(0x0)


def play(times):
    global turns

    while times != 0:
        turns = 0

        deal_cards(shuffle_cards(generate_cards()))

        while not check_len():
            smart_pull(turns), handle_cards()
            turns += 1

        print('%s turns to complete the game' % turns)
        times -= 1
