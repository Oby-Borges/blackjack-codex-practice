import random
import time

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
CARD_VALUES = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11,
}

PLAYER_DRAW_DELAY = 1.2
DEALER_TURN_DELAY = 1.5
DEALER_DRAW_DELAY = 1.2
RESULT_DELAY = 1.0


def create_deck():
    """Create a standard 52-card deck."""
    return [(rank, suit) for suit in SUITS for rank in RANKS]



def shuffle_deck(deck):
    """Shuffle the deck in place."""
    random.shuffle(deck)



def deal_card(deck):
    """Remove and return the top card from the deck."""
    return deck.pop()



def card_to_string(card):
    """Convert a card tuple into a friendly string."""
    rank, suit = card
    return f"{rank} of {suit}"



def calculate_hand_value(hand):
    """Return the best Blackjack value for a hand, treating aces as 1 or 11."""
    total = 0
    aces = 0

    for rank, _ in hand:
        total += CARD_VALUES[rank]
        if rank == "A":
            aces += 1

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total



def is_blackjack(hand):
    """Return True if the hand is a natural blackjack."""
    return len(hand) == 2 and calculate_hand_value(hand) == 21



def print_divider():
    """Print a simple divider for cleaner output."""
    print("\n" + "=" * 40)



def display_hand(name, hand, hide_first_card=False):
    """Print a hand of cards and its visible total."""
    print(f"{name}'s hand:")

    for index, card in enumerate(hand, start=1):
        if hide_first_card and index == 1:
            print("  1. Hidden card")
        else:
            print(f"  {index}. {card_to_string(card)}")

    if hide_first_card:
        visible_total = calculate_hand_value(hand[1:])
        print(f"Visible total: {visible_total}+")
    else:
        print(f"Total: {calculate_hand_value(hand)}")



def get_player_choice():
    """Ask the player whether to hit or stand."""
    while True:
        choice = input("\nDo you want to hit or stand? (h/s): ").strip().lower()
        if choice in {"h", "hit"}:
            return "hit"
        if choice in {"s", "stand"}:
            return "stand"
        print("Please type 'h' for hit or 's' for stand.")



def ask_to_play_again():
    """Ask the player if they want to play another round."""
    while True:
        choice = input("\nWould you like to play another round? (y/n): ").strip().lower()
        if choice in {"y", "yes"}:
            return True
        if choice in {"n", "no"}:
            return False
        print("Please type 'y' for yes or 'n' for no.")



def determine_winner(player_value, dealer_value):
    """Return the outcome message based on Blackjack rules."""
    if player_value > 21:
        return "You bust. Dealer wins!"
    if dealer_value > 21:
        return "Dealer busts. You win!"
    if player_value > dealer_value:
        return "You win!"
    if dealer_value > player_value:
        return "Dealer wins!"
    return "Push! It's a tie."



def show_final_result(player_hand, dealer_hand, message):
    """Display the full results for the round."""
    time.sleep(RESULT_DELAY)
    print_divider()
    print("Final hands")
    print("-" * 40)
    display_hand("Player", player_hand)
    print()
    display_hand("Dealer", dealer_hand)
    print(f"\nResult: {message}")
    print_divider()



def play_round(round_number):
    """Run one round of Blackjack."""
    print_divider()
    print(f"Round {round_number}")
    print_divider()

    deck = create_deck()
    shuffle_deck(deck)

    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]

    display_hand("Dealer", dealer_hand, hide_first_card=True)
    print()
    display_hand("Player", player_hand)

    player_has_blackjack = is_blackjack(player_hand)
    dealer_has_blackjack = is_blackjack(dealer_hand)

    if player_has_blackjack or dealer_has_blackjack:
        if player_has_blackjack and dealer_has_blackjack:
            result = "Both you and the dealer have blackjack. Push!"
        elif player_has_blackjack:
            result = "Blackjack! You win!"
        else:
            result = "Dealer has blackjack. Dealer wins!"

        show_final_result(player_hand, dealer_hand, result)
        return

    while calculate_hand_value(player_hand) < 21:
        if get_player_choice() == "stand":
            break

        print("\nYou chose to hit...")
        time.sleep(PLAYER_DRAW_DELAY)
        new_card = deal_card(deck)
        player_hand.append(new_card)
        print(f"You drew: {card_to_string(new_card)}")
        print()
        display_hand("Player", player_hand)

    player_value = calculate_hand_value(player_hand)
    if player_value > 21:
        show_final_result(player_hand, dealer_hand, determine_winner(player_value, calculate_hand_value(dealer_hand)))
        return

    print("\nDealer's turn...")
    time.sleep(DEALER_TURN_DELAY)
    display_hand("Dealer", dealer_hand)

    while calculate_hand_value(dealer_hand) < 17:
        time.sleep(DEALER_DRAW_DELAY)
        new_card = deal_card(deck)
        dealer_hand.append(new_card)
        print(f"\nDealer draws: {card_to_string(new_card)}")
        display_hand("Dealer", dealer_hand)

    dealer_value = calculate_hand_value(dealer_hand)
    result = determine_winner(player_value, dealer_value)
    show_final_result(player_hand, dealer_hand, result)



def play_blackjack():
    """Run Blackjack in the terminal with multiple rounds."""
    print("Welcome to Blackjack!")

    round_number = 1
    while True:
        play_round(round_number)
        round_number += 1

        if not ask_to_play_again():
            print("\nThanks for playing!")
            break


if __name__ == "__main__":
    play_blackjack()
