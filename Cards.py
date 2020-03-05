# Kaden Barnes
# February 27, 2020
# Card Module: Contains deck creation and shuffling functions, and hand
# dealing and evaluation functions.
 
# Imports
import random
 
# Functions


##########################################################
# Shuffling and stack-handling functions
def create_deck(shuffled): # Create and return a fresh deck.
    newDeck = []
    for i in range(52):
        newDeck.append(i)
    if shuffled == True:
        random.shuffle(newDeck)
    return newDeck

# Take a variable number of stacks, shuffles them all into the first given stack,
# then returns this new combined stack.
def shuffle_deck(stack, *stacks):
    allStacks = flatten_list(list(stacks))
    for i in range(len(allStacks)):
        stack.append(allStacks[i])
    random.shuffle(stack)
    return stack

# Deals with the tuple from our variadic shuffling function above
def flatten_list(listList):
    flatList = []
    x = len(listList)
    for i in range(x):
        y = len(listList[i])
        p = listList[i]
        for j in range(y):
            flatList.append(p[j])

    return flatList

# Take one stack of cards, deal the top 5 into a new list.
def deal_hand(stack1):
    stack2 = []
    for i in range(5):
        stack2.append(stack1[0])
        stack1.remove(stack1[0])
    return stack2

# Takes a card, returns its value
def card_value(val): 
    if val in range(13,26):
        val -= 13
    if val in range(26,39):
        val -= 26
    if val in range(39,52):
        val -= 39
    return val

# Takes a card, returns its suit
def card_suit(card):
    if card in range(0,13):
        suit = 0
    elif card in range(13,26):
        suit = 1
    elif card in range(26,39):
        suit = 2
    else:
        suit = 3
    return suit

# Takes a stack and return just the suits of each card.
def suit_stack(stack):
    suitStack = []
    for i in range(len(stack)):
        suitStack.append(card_suit(stack[i]))
    return suitStack

# Takes a stack and return just the values of each card.    
def val_stack(stack):
    valStack = []
    for i in range(len(stack)):
        valStack.append(card_value(stack[i]))
    valStack.sort()
    return valStack

# Takes a stack and converts each card into a string of its value.
def convert_to_english(stack):
    englishStack = []
    valStack = val_stack(stack)
    suitStack = suit_stack(stack)
    for i in range(len(stack)):
        card = cardsValEng[valStack[i]] + cardsSuitEng[suitStack[i]]
        englishStack.append(card)

    return englishStack

# Takes a stack and converts each card into a simple representation (A♠)
def convert_to_simple(stack):
    simpleStack = []
    valStack = val_stack(stack)
    suitStack = suit_stack(stack)
    for i in range(len(stack)):
        card = cardsValSimple[valStack[i]] + cardsSuitSimple[suitStack[i]]
        simpleStack.append(card)

    return simpleStack

########################################################
# Hand-evaluation functions

# Evaluate a given stack for valid poker hands.
# Doesn't return straight away - calculates everything and then returns - should be modified in the future to return immediately.
def check_hand(stack):
    # Get the values and suits, and sort the values list for later.
    valList = val_stack(stack)
    valList.sort()
    suitList = suit_stack(stack)
    
    if len(set(suitList)) == 1:
        flush = True
    else:
        flush = False

    # If there's only two distinct values of cards in the hand,
    # we check whether it's a four of a kind or full house.
    if len(set(valList)) == 2:
        if valList[2] == valList[3] and valList[2] == valList[1]:
            fourOfKind = True
        else:
            fullHouse = True
            fourOfKind = False
    else:
        fourOfKind = False
        fullHouse = False

    # If there's three distinct values, it could be three of a kind
    # or two pair.
    if len(set(valList)) == 3:
        if (valList[2] == valList[1] and valList[0] == valList[2]) or (valList[2] == valList[3] and valList[2] == valList[4]) or (valList[2] == valList[3] and valList[1] == valList[3]):
            threeOfKind = True
        else:
            twoPair = True
            threeOfKind = False
    else:
        threeOfKind = False
        twoPair = False

    # If there's 4 distinct values we know there's one pair.
    if len(set(valList)) == 4:
        onePair = True
    else:
        onePair = False

    # Check whether the cards are in sequential order to determine if
    # they're a straight or not - then check for a royal straight.
    if(valList[0]+1 == valList[1] and valList[1]+1 == valList[2] and valList[2]+1 == valList[3] and valList[3]+1 == valList[4]) or (valList[0]+9 == valList[1]and valList[1]+1 == valList[2] and valList[2]+1 == valList[3] and valList[3]+1 == valList[4]):
        straight = True
        if valList[0] == 0:
            royal = True
        else:
            royal = False
    else:
        straight = False
        royal = False
    
    # Return what the highest scoring poker hand is.
    if royal == True and flush == True:
        return "Royal Flush"
    elif straight == True and flush == True:
        return "Straight Flush"
    elif fourOfKind == True:
        return "Four of a Kind"
    elif fullHouse == True:
        return "Full House"
    elif flush == True:
        return "Flush"
    elif straight == True:
        return "Straight"
    elif threeOfKind == True:
        return "Three of a Kind"
    elif twoPair == True:
        return "Two Pair"
    elif onePair == True:
        return "One Pair"
    else:
        return "High Card"

# Using the values of the cards, creates a string that corresponds to the
# hand's value. First gives the matching (duplicate) cards in descending
# order, then the highest nonmatching cards. This should prevent ties in most cases.
def high_card(stack):
    nonDupList = []
    valList = val_stack(stack)
    offset = 0
    cardString = ""
    for i in range(len(stack)):
        if valList.count(valList[offset]) == 1:
            nonDupList.append(valList[offset])
            valList.pop(offset)
        else:
            offset += 1
    
    valList = list(set(valList))

    # Deals with aces. Since aces are value zero but in actuality the highest card,
    # we need to put them at the end of the list before we reverse it so they'll be
    # in the right place.
    # Probably a better/simpler solution for this but I don't want to bother finding it ATM
    if len(valList) > 0:
        if valList[0] == 0:
            valList.append(valList[0])
            valList.pop(valList[0])
    if len(nonDupList) > 0:
        if nonDupList[0] == 0:
            nonDupList.append(nonDupList[0])
            nonDupList.pop(nonDupList[0])
    
    nonDupList.reverse()
    valList.reverse()

    # Loops to repeatedly add on to cardString
    if len(valList) == 0:
        for i in range(len(nonDupList)):
            cardString = cardString + pokerHighCardStr[nonDupList[i]]
    elif len(nonDupList) == 0:
        for i in range(len(valList)):
            cardString = cardString + pokerHighCardStr[valList[i]]
    else:
        
        for i in range(len(valList)):
            cardString = cardString + pokerHighCardStr[valList[i]]
        for i in range(len(nonDupList)):
            cardString = cardString + pokerHighCardStr[nonDupList[i]]

    return cardString
    

# Simple function for testing a certain number of hands
def test_hands(deck, trials):
    handsList = [0,0,0,0,0,0,0,0,0,0]
    for i in range(trials):
        hand = deal_hand(deck) 
        print(convert_to_simple(hand))
        pokerHand = check_hand(hand)
        print(pokerHand)

        # Frequency list for different hands
        if pokerHand == "Royal Flush":
            handsList[0] += 1
        elif pokerHand == "Straight Flush":
            handsList[1] += 1
        elif pokerHand == "Four of a Kind":
            handsList[2] += 1
        elif pokerHand == "Full House":
            handsList[3] += 1
        elif pokerHand == "Flush":
            handsList[4] += 1
        elif pokerHand == "Straight":
            handsList[5] += 1
        elif pokerHand == "Three of a Kind":
            handsList[6] += 1
        elif pokerHand == "Two Pair":
            handsList[7] += 1
        elif pokerHand == "One Pair":
            handsList[8] += 1
        else:
            handsList[9] += 1
        
        shuffle_deck(deck, hand)

        print("")
    print(handsList)
    ratioList = []
    for i in range(10):
        ratioList.append(handsList[i]/trials)
    print(ratioList)

def hand_value(stack):
    return pokerHandsStr[check_hand(stack)] + high_card(stack)

# Compare the string value derived from hand_value() of two different hands to see which beats which.
def compare_hands(stack1, stack2):
    hand1Val = hand_value(stack1)
    hand2Val = hand_value(stack2)
    #print(hand1Val + " ~~ " + hand2Val) # Testing function for seeing the hand_value string for each hand
    if hand1Val > hand2Val:
        print("Hand 1 wins!")
    elif hand1Val < hand2Val:
        print("Hand 2 wins!")
    else:
        print("What on Earth?! They're equal!")

# Function for testing the compare_hands() function a given number of times.
def test_compare_hands(deck, trials):
    for i in range(trials):
        hand1 = deal_hand(deck)
        hand2 = deal_hand(deck)
        print("Hand 1: ",  convert_to_simple(hand1))
        print(check_hand(hand1))
        print("Hand 2: ",  convert_to_simple(hand2))
        print(check_hand(hand2))
        print("")
        compare_hands(hand1,hand2)
        print("")

        shuffle_deck(deck, hand1, hand2)
    
########################################
# Card dictionaries
cardsValEng = {0: "Ace of ", 1: "Two of ", 2: "Three of ", 3: "Four of ", 4: "Five of ",
            5: "Six of ", 6: "Seven of ", 7: "Eight of ", 8: "Nine of ", 9: "Ten of ",
            10: "Jack of ", 11: "Queen of ", 12: "King of ", }
cardsSuitEng = {0: "Spades", 1: "Hearts", 2: "Clubs", 3: "Diamonds"}
 
cardsValSimple = {0: "A", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6", 6: "7", 7: "8", 8: "9", 9: "10", 10: "J", 11: "Q", 12: "K", }
cardsSuitSimple = {0: "♠", 1: "♥", 2: "♣", 3: "♦"}

pokerHandsStr = {
                "High Card": "0", "One Pair": "1", "Two Pair": "2", "Three of a Kind": "3",
                "Straight": "4", "Flush": "5", "Full House": "6", "Four of a Kind": "7",
                "Straight Flush": "8", "Royal Flush": "9"
                }
pokerHighCardStr = { 0: "x", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h", 8: "i", 9: "j", 10: "k", 11: "l", 12: "m" }


#####################################################################
#####################################################################



# main()
def main():
    deck = create_deck(True) # Create a shuffled deck

    # test_hands(deck, 20)
    test_compare_hands(deck, 20)
        
    
main()
