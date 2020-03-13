# Kaden Barnes
# March 12, 2020
# Blackjack game

# Imports
import Cards as cds

# Functions


# def main()
def main():
	deck = cds.create_deck(True)
	dealerh = cds.deal_hand(deck, 2)
	print(dealerh)

main()