import os
import random
import time

from colorama import Fore, Style, init

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
SUIT_SYMBOLS = {
    "Spades": "♠",
    "Hearts": "♥",
    "Diamonds": "♦",
    "Clubs": "♣",
}
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
TYPEWRITER_DELAY = 0.04
SHORT_PAUSE = 0.5
MEDIUM_PAUSE = 0.9
REVEAL_PAUSE = 1.1
RESULT_PAUSE = 0.9

PLAYER_COLOR = Fore.CYAN
DEALER_COLOR = Fore.BLUE
WIN_COLOR = Fore.GREEN
LOSS_COLOR = Fore.RED
PUSH_COLOR = Fore.YELLOW
PROMPT_COLOR = Fore.WHITE
SYSTEM_COLOR = Fore.WHITE

init(autoreset=True)


def typewriter_print(message, color=SYSTEM_COLOR, delay=TYPEWRITER_DELAY, end="\n"):
    """Print text one character at a time with optional color styling."""
    styled_message = f"{color}{message}{Style.RESET_ALL}"
    for character in styled_message:
        print(character, end="", flush=True)
        time.sleep(delay)
    if end:
        print(end=end, flush=True)



def typewriter_input(prompt, color=PROMPT_COLOR):
    """Display a prompt with the typewriter effect and capture input cleanly."""
    typewriter_print(prompt, color=color, end="")
    return input().strip()



def pause(seconds=SHORT_PAUSE):
    """Pause briefly to improve pacing."""
    time.sleep(seconds)



def clear_screen():
    """Clear the terminal between rounds when possible."""
    os.system("cls" if os.name == "nt" else "clear")



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
    """Convert a card tuple into a compact display string."""
    rank, suit = card
    return f"{rank}{SUIT_SYMBOLS[suit]}"



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



def print_divider(color=SYSTEM_COLOR):
    """Print a simple divider for cleaner output."""
    typewriter_print("=" * 40, color=color)



def format_hand(name, hand, hide_first_card=False):
    """Return a clean hand display string."""
    if hide_first_card:
        visible_cards = [card_to_string(hand[1]), "[?]"] if len(hand) > 1 else ["[?]"]
        return f"{name}: {', '.join(visible_cards)}"

    cards_text = ", ".join(card_to_string(card) for card in hand)
    return f"{name}: {cards_text} ({calculate_hand_value(hand)})"



def display_hand(name, hand, color, hide_first_card=False):
    """Display a formatted hand with the typewriter effect."""
    typewriter_print(format_hand(name, hand, hide_first_card=hide_first_card), color=color)



def show_round_header(round_number, chips, bet):
    """Display an animated header for the round."""
    print_divider()
    typewriter_print("♠ ♥ ♦ ♣  BLACKJACK  ♣ ♦ ♥ ♠", color=WIN_COLOR)
    typewriter_print(f"Round {round_number}", color=SYSTEM_COLOR)
    typewriter_print(f"Chips: {chips} | Bet: {bet}", color=PLAYER_COLOR)
    print_divider()



def get_bet(chips):
    """Ask the player how many chips they want to bet."""
    while True:
        print_divider()
        typewriter_print(f"Current chips: {chips}", color=PLAYER_COLOR)
        bet_text = typewriter_input("Enter your bet for this round: ", color=PROMPT_COLOR)

        if not bet_text.isdigit():
            typewriter_print("Please enter a positive whole number.", color=LOSS_COLOR)
            continue

        bet = int(bet_text)
        if bet <= 0:
            typewriter_print("Your bet must be at least 1 chip.", color=LOSS_COLOR)
            continue
        if bet > chips:
            typewriter_print("You cannot bet more chips than you have.", color=LOSS_COLOR)
            continue

        return bet



def get_player_choice():
    """Ask the player whether to hit or stand."""
    while True:
        choice = typewriter_input("Do you want to hit or stand? (h/s): ", color=PROMPT_COLOR).lower()
        if choice in {"h", "hit"}:
            return "hit"
        if choice in {"s", "stand"}:
            return "stand"
        typewriter_print("Please type 'h' for hit or 's' for stand.", color=LOSS_COLOR)



def ask_to_play_again():
    """Ask the player if they want to play another round."""
    while True:
        choice = typewriter_input("Would you like to play another round? (y/n): ", color=PROMPT_COLOR).lower()
        if choice in {"y", "yes"}:
            return True
        if choice in {"n", "no"}:
            return False
        typewriter_print("Please type 'y' for yes or 'n' for no.", color=LOSS_COLOR)



def offer_chip_refill():
    """Offer the player a refill when they run out of chips."""
    while True:
        choice = typewriter_input("You're out of chips. Refill to 100? (y/n): ", color=PROMPT_COLOR).lower()
        if choice in {"y", "yes"}:
            typewriter_print("Chips refilled to 100. Back to the table!", color=WIN_COLOR)
            return STARTING_CHIPS
        if choice in {"n", "no"}:
            typewriter_print("Thanks for playing Blackjack. See you next time!", color=SYSTEM_COLOR)
            return 0
        typewriter_print("Please type 'y' for yes or 'n' for no.", color=LOSS_COLOR)



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
    """Return a final message and color for the outcome."""
    if player_blackjack and dealer_blackjack:
        return "Both you and the dealer have blackjack. Push!", PUSH_COLOR
    if player_blackjack:
        return "Blackjack! You win!", WIN_COLOR
    if dealer_blackjack:
        return "Dealer has blackjack. Dealer wins!", LOSS_COLOR
    if outcome == "player":
        return "You win!", WIN_COLOR
    if outcome == "dealer":
        return "Dealer wins!", LOSS_COLOR
    return "Push! It's a tie.", PUSH_COLOR



def settle_bet(chips, bet, outcome):
    """Return the updated chip total after the round."""
    if outcome == "player":
        return chips + bet
    if outcome == "dealer":
        return chips - bet
    return chips



def show_chip_update(chips):
    """Display the chip total after a round."""
    chip_color = WIN_COLOR if chips > 0 else LOSS_COLOR
    typewriter_print(f"Chips after this round: {chips}", color=chip_color)



def show_final_result(player_hand, dealer_hand, result_message, result_color, chips, bet):
    """Display the full results for the round."""
    pause(RESULT_PAUSE)
    print_divider()
    typewriter_print("Final hands", color=SYSTEM_COLOR)
    typewriter_print("-" * 40, color=SYSTEM_COLOR)
    display_hand("Player", player_hand, PLAYER_COLOR)
    display_hand("Dealer", dealer_hand, DEALER_COLOR)
    pause(0.5)
    typewriter_print(f"Result: {result_message}", color=result_color)
    show_chip_update(chips)
    typewriter_print(f"Bet this round: {bet}", color=PLAYER_COLOR)
    print_divider()



def player_turn(deck, player_hand):
    """Handle the player's turn and return the final hand."""
    while calculate_hand_value(player_hand) < 21:
        choice = get_player_choice()

        if choice == "stand":
            typewriter_print("You stand.", color=PLAYER_COLOR)
            pause()
            break

        typewriter_print("You choose to hit.", color=PLAYER_COLOR)
        pause(0.35)
        typewriter_print("Dealing your next card...", color=SYSTEM_COLOR)
        pause(0.6)
        new_card = deal_card(deck)
        player_hand.append(new_card)
        typewriter_print(f"You drew {card_to_string(new_card)}.", color=PLAYER_COLOR)
        pause(0.35)
        display_hand("Player", player_hand, PLAYER_COLOR)

        if calculate_hand_value(player_hand) >= 21:
            break

    return player_hand



def dealer_turn(deck, dealer_hand):
    """Handle the dealer's turn and return the final hand."""
    typewriter_print("Dealer reveals the hidden card...", color=DEALER_COLOR)
    pause(REVEAL_PAUSE)
    display_hand("Dealer", dealer_hand, DEALER_COLOR)

    while calculate_hand_value(dealer_hand) < 17:
        pause(0.6)
        typewriter_print("Dealer hits...", color=DEALER_COLOR)
        pause(0.6)
        new_card = deal_card(deck)
        dealer_hand.append(new_card)
        typewriter_print(f"Dealer drew {card_to_string(new_card)}.", color=DEALER_COLOR)
        pause(0.35)
        display_hand("Dealer", dealer_hand, DEALER_COLOR)

    if calculate_hand_value(dealer_hand) >= 17:
        pause(0.4)
        typewriter_print("Dealer stands.", color=DEALER_COLOR)

    return dealer_hand



def play_round(round_number, chips):
    """Run one round of Blackjack and return the updated chip count."""
    clear_screen()
    bet = get_bet(chips)
    show_round_header(round_number, chips, bet)

    deck = create_deck()
    shuffle_deck(deck)

    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]

    display_hand("Dealer", dealer_hand, DEALER_COLOR, hide_first_card=True)
    display_hand("Player", player_hand, PLAYER_COLOR)

    player_has_blackjack = is_blackjack(player_hand)
    dealer_has_blackjack = is_blackjack(dealer_hand)

    if player_has_blackjack or dealer_has_blackjack:
        outcome = determine_winner(calculate_hand_value(player_hand), calculate_hand_value(dealer_hand))
        result, result_color = outcome_message(outcome, player_has_blackjack, dealer_has_blackjack)
        updated_chips = settle_bet(chips, bet, outcome)
        show_final_result(player_hand, dealer_hand, result, result_color, updated_chips, bet)
        return updated_chips

    player_turn(deck, player_hand)
    player_value = calculate_hand_value(player_hand)

    if player_value > 21:
        result = "You bust. Dealer wins!"
        updated_chips = settle_bet(chips, bet, "dealer")
        show_final_result(player_hand, dealer_hand, result, LOSS_COLOR, updated_chips, bet)
        return updated_chips

    typewriter_print("Dealer's turn...", color=DEALER_COLOR)
    pause(MEDIUM_PAUSE)
    dealer_turn(deck, dealer_hand)

    dealer_value = calculate_hand_value(dealer_hand)
    outcome = determine_winner(player_value, dealer_value)

    if dealer_value > 21:
        result = "Dealer busts. You win!"
        result_color = WIN_COLOR
    else:
        result, result_color = outcome_message(outcome)

    updated_chips = settle_bet(chips, bet, outcome)
    show_final_result(player_hand, dealer_hand, result, result_color, updated_chips, bet)
    return updated_chips



def play_blackjack():
    """Run Blackjack in the terminal with multiple rounds."""
    clear_screen()
    print_divider(WIN_COLOR)
    typewriter_print("Welcome to Blackjack!", color=WIN_COLOR)
    typewriter_print("Try your luck and beat the dealer.", color=SYSTEM_COLOR)
    print_divider(WIN_COLOR)

    chips = STARTING_CHIPS
    round_number = 1

    while True:
        chips = play_round(round_number, chips)
        round_number += 1

        if chips <= 0:
            chips = offer_chip_refill()
            if chips <= 0:
                break
            continue

        if not ask_to_play_again():
            typewriter_print("Thanks for playing Blackjack. Goodbye!", color=SYSTEM_COLOR)
            break


if __name__ == "__main__":
    play_blackjack()
