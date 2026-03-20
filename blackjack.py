import random

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



def display_hand(name, hand, hide_first_card=False):
    """Print a hand of cards."""
    print(f"\n{name}'s hand:")
    for index, card in enumerate(hand):
        if hide_first_card and index == 0:
            print("- Hidden card")
        else:
            print(f"- {card_to_string(card)}")



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



def get_player_choice():
    """Ask the player whether to hit or stand."""
    while True:
        choice = input("\nDo you want to hit or stand? (h/s): ").strip().lower()
        if choice in {"h", "hit"}:
            return "hit"
        if choice in {"s", "stand"}:
            return "stand"
        print("Please type 'h' for hit or 's' for stand.")



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



def play_blackjack():
    """Run one round of Blackjack in the terminal."""
    print("Welcome to Blackjack!")

    deck = create_deck()
    shuffle_deck(deck)

    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]

    display_hand("Dealer", dealer_hand, hide_first_card=True)
    display_hand("Player", player_hand)
    print(f"Player total: {calculate_hand_value(player_hand)}")

    while calculate_hand_value(player_hand) < 21:
        if get_player_choice() == "stand":
            break

        new_card = deal_card(deck)
        player_hand.append(new_card)
        print(f"\nYou drew: {card_to_string(new_card)}")
        display_hand("Player", player_hand)
        print(f"Player total: {calculate_hand_value(player_hand)}")

    player_value = calculate_hand_value(player_hand)
    if player_value <= 21:
        print("\nDealer's turn...")
        display_hand("Dealer", dealer_hand)
        print(f"Dealer total: {calculate_hand_value(dealer_hand)}")

        while calculate_hand_value(dealer_hand) < 17:
            new_card = deal_card(deck)
            dealer_hand.append(new_card)
            print(f"Dealer draws: {card_to_string(new_card)}")
            print(f"Dealer total: {calculate_hand_value(dealer_hand)}")

    dealer_value = calculate_hand_value(dealer_hand)

    print("\nFinal hands:")
    display_hand("Player", player_hand)
    print(f"Player total: {player_value}")
    display_hand("Dealer", dealer_hand)
    print(f"Dealer total: {dealer_value}")

    print(f"\n{determine_winner(player_value, dealer_value)}")


if __name__ == "__main__":
    play_blackjack()
