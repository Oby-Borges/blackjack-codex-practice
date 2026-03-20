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

STARTING_CHIPS = 100
TYPEWRITER_DELAY = 0.02
SHORT_PAUSE = 0.5
MEDIUM_PAUSE = 0.8


def typewriter_print(message, delay=TYPEWRITER_DELAY):
    """Print text one character at a time for a simple animated effect."""
    for character in message:
        print(character, end="", flush=True)
        time.sleep(delay)
    print()



def pause(seconds=SHORT_PAUSE):
    """Pause briefly to make events feel more step-by-step."""
    time.sleep(seconds)



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



def show_round_header(round_number, chips, bet):
    """Display an animated header for the round."""
    print_divider()
    typewriter_print(f"Round {round_number}")
    typewriter_print(f"Chips: {chips} | Bet: {bet}")
    print_divider()



def get_bet(chips):
    """Ask the player how many chips they want to bet."""
    while True:
        print_divider()
        print(f"Current chips: {chips}")
        bet_text = input("Enter your bet for this round: ").strip()

        if not bet_text.isdigit():
            print("Please enter a positive whole number.")
            continue

        bet = int(bet_text)
        if bet <= 0:
            print("Your bet must be at least 1 chip.")
            continue
        if bet > chips:
            print("You cannot bet more chips than you have.")
            continue

        return bet



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
        return "dealer"
    if dealer_value > 21:
        return "player"
    if player_value > dealer_value:
        return "player"
    if dealer_value > player_value:
        return "dealer"
    return "push"



def outcome_message(outcome, player_blackjack=False, dealer_blackjack=False):
    """Return a friendly final message for the outcome."""
    if player_blackjack and dealer_blackjack:
        return "Both you and the dealer have blackjack. Push!"
    if player_blackjack:
        return "Blackjack! You win!"
    if dealer_blackjack:
        return "Dealer has blackjack. Dealer wins!"
    if outcome == "player":
        return "You win!"
    if outcome == "dealer":
        return "Dealer wins!"
    return "Push! It's a tie."



def settle_bet(chips, bet, outcome):
    """Return the updated chip total after the round."""
    if outcome == "player":
        return chips + bet
    if outcome == "dealer":
        return chips - bet
    return chips



def show_final_result(player_hand, dealer_hand, result_message, chips, bet):
    """Display the full results for the round."""
    pause(MEDIUM_PAUSE)
    print_divider()
    print("Final hands")
    print("-" * 40)
    display_hand("Player", player_hand)
    print()
    display_hand("Dealer", dealer_hand)
    print()
    typewriter_print(f"Result: {result_message}")

    if chips > 0:
        print(f"Chips after this round: {chips}")
    else:
        print(f"Chips after this round: 0")

    print(f"Bet this round: {bet}")
    print_divider()



def player_turn(deck, player_hand):
    """Handle the player's turn and return the final hand."""
    while calculate_hand_value(player_hand) < 21:
        choice = get_player_choice()

        if choice == "stand":
            typewriter_print("You chose to stand.")
            pause()
            break

        typewriter_print("You chose to hit.")
        pause(0.35)
        typewriter_print("Drawing a card...")
        pause(0.6)
        new_card = deal_card(deck)
        player_hand.append(new_card)
        typewriter_print(f"You drew: {card_to_string(new_card)}")
        pause(0.35)
        display_hand("Player", player_hand)

        if calculate_hand_value(player_hand) >= 21:
            break

    return player_hand



def dealer_turn(deck, dealer_hand):
    """Handle the dealer's turn and return the final hand."""
    typewriter_print("Dealer reveals the hidden card...")
    pause(MEDIUM_PAUSE)
    display_hand("Dealer", dealer_hand)

    while calculate_hand_value(dealer_hand) < 17:
        pause(0.6)
        typewriter_print("Dealer draws a card...")
        pause(0.6)
        new_card = deal_card(deck)
        dealer_hand.append(new_card)
        typewriter_print(f"Dealer drew: {card_to_string(new_card)}")
        pause(0.35)
        display_hand("Dealer", dealer_hand)

    return dealer_hand



def play_round(round_number, chips):
    """Run one round of Blackjack and return the updated chip count."""
    bet = get_bet(chips)
    show_round_header(round_number, chips, bet)

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
        outcome = determine_winner(calculate_hand_value(player_hand), calculate_hand_value(dealer_hand))
        result = outcome_message(outcome, player_has_blackjack, dealer_has_blackjack)
        updated_chips = settle_bet(chips, bet, outcome)
        show_final_result(player_hand, dealer_hand, result, updated_chips, bet)
        return updated_chips

    player_turn(deck, player_hand)
    player_value = calculate_hand_value(player_hand)

    if player_value > 21:
        result = "You bust. Dealer wins!"
        updated_chips = settle_bet(chips, bet, "dealer")
        show_final_result(player_hand, dealer_hand, result, updated_chips, bet)
        return updated_chips

    typewriter_print("Dealer's turn...")
    pause(MEDIUM_PAUSE)
    dealer_turn(deck, dealer_hand)

    dealer_value = calculate_hand_value(dealer_hand)
    outcome = determine_winner(player_value, dealer_value)

    if dealer_value > 21:
        result = "Dealer busts. You win!"
    else:
        result = outcome_message(outcome)

    updated_chips = settle_bet(chips, bet, outcome)
    show_final_result(player_hand, dealer_hand, result, updated_chips, bet)
    return updated_chips



def play_blackjack():
    """Run Blackjack in the terminal with multiple rounds."""
    typewriter_print("Welcome to Blackjack!")

    chips = STARTING_CHIPS
    round_number = 1

    while chips > 0:
        chips = play_round(round_number, chips)
        round_number += 1

        if chips <= 0:
            typewriter_print("You ran out of chips. Game over!")
            break

        if not ask_to_play_again():
            typewriter_print("Thanks for playing!")
            break


if __name__ == "__main__":
    play_blackjack()
