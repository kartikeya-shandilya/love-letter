#!/usr/bin/env python

from random import shuffle, randint
from operator import itemgetter
from collections import Counter, defaultdict

from get_action import get_action
from utilities import determine_winner, print_deck, score, prep_perfdict, valid_moves
from strategy_bandit import strategy_bandit

def game_step(move, A, B, CARDS, SEEN, hmaid_A, hmaid_B, known_A, known_B, PRINT, strategy=defaultdict()):
	
	choices = None
	drop = None
	
	deck = Counter(SEEN)
	deck = sorted(deck.items(), key=itemgetter(0))
	
	KNOWNS = (known_A, known_B)
	if move == 'B':
		KNOWNS = (known_B, known_A)
	
	HMAID = hmaid_B
	if move == 'B':
		HMAID = hmaid_A
	
	if move == 'A':
		A.append(CARDS.pop(0))
		choices = A[:]
		#if PRINT: print "Player A's turn, your cards: ",A,"\n","Enter the card that you'd like to drop: ",
		if PRINT: print "Player A's turn, cards are:", A
		#drop = int(raw_input())
		#if drop in range(12,19): A.remove(1)
		#elif drop in range(50,52): A.remove(5)
		#else: A.remove(drop)
		drop_ops = valid_moves(choices)
		try:
			#print "trying this key :::", (str(sorted(choices)),str(KNOWNS),HMAID,str(deck))
			strat_dict = strategy[(str(sorted(choices)),str(KNOWNS),HMAID,str(deck))]
		except:
			strat_dict = {}
		perf_dict = prep_perfdict(drop_ops, strat_dict)
		if PRINT: print "Perf-dict from known experiments:", perf_dict
		drop = strategy_bandit(perf_dict, "eps-greedy")
		if drop>10: A.remove(drop/10)
		else:		A.remove(drop)
		if drop == known_B or drop/10 == known_B:
			known_B = 0
		if PRINT: print "Card chosen to drop:", drop
		A, B, CARDS, hmaid_A, known_A, known_B, win_flag, xtr_drop = get_action('A', A, B, CARDS, drop, hmaid_B, known_A, known_B)
	
	else:
		B.append(CARDS.pop(0))
		choices = B[:]
		if PRINT: print "Player B's turn, your cards: ",B,"\n","Enter the card that you'd like to drop: ",
		drop = int(raw_input())
		if drop in range(12,19): B.remove(1)
		elif drop in range(50,52): B.remove(5)
		else: B.remove(drop)
		"""drop_ops = valid_moves(choices)
		try:
			#print "trying this key :::", (str(sorted(choices)),str(KNOWNS),HMAID,str(deck))
			strat_dict = strategy[(str(sorted(choices)),str(KNOWNS),HMAID,str(deck))]
		except:
			strat_dict = {}
		perf_dict = prep_perfdict(drop_ops, strat_dict)
		if PRINT: print "Perf-dict from known experiments:", perf_dict
		drop = strategy_bandit(perf_dict, "eps-greedy")
		if drop>10: B.remove(drop/10)
		else:		B.remove(drop)"""
		if drop == known_A or drop/10 == known_A:
			known_A = 0
		if PRINT: print "Card chosen to drop:", drop
		A, B, CARDS, hmaid_B, known_A, known_B, win_flag, xtr_drop = get_action('B', A, B, CARDS, drop, hmaid_A, known_A, known_B)
	
	choices.sort()
	
	tmpdrop = drop
	if drop>10: tmpdrop/=10
	SEEN.append(tmpdrop)
	if xtr_drop:
		SEEN.append(xtr_drop)

	return A, B, CARDS, SEEN, hmaid_A, hmaid_B, known_A, known_B, win_flag, (move, str(choices), str(KNOWNS), HMAID, str(deck), drop)


def game_setup():
	
	# shuffle cards
	CARDS = [1,1,1,1,1,2,2,3,3,4,4,5,5,6,7,8]
	shuffle(CARDS)
	SEEN = CARDS[-3:][:]
	CARDS = CARDS[:-3]
	
	# deal first hand cards
	A = [CARDS.pop(0)]
	B = [CARDS.pop(0)]
	
	# initialize last drop actions
	hmaid_A = False
	hmaid_B = False

	# initialize known statuses
	known_A = 0 # A knows what B has
	known_B = 0 # B knows what A has
	
	# win flag
	win_flag = None
	
	# game_states
	game_states = []

	cnt = 0

	return CARDS, SEEN, A, B, hmaid_A, hmaid_B, known_A, known_B, win_flag, game_states, cnt


def test_step(move, A, B, CARDS, SEEN, hmaid_A, hmaid_B, known_A, known_B, strategy, arg="Random"):
	
	choices = None
	drop = None
	
	deck = Counter(SEEN)
	deck = sorted(deck.items(), key=itemgetter(0))
	
	KNOWNS = (known_A, known_B)
	if move == 'B':
		KNOWNS = (known_B, known_A)
	
	HMAID = hmaid_B
	if move == 'B':
		HMAID = hmaid_A
	
	if move == 'A':
		A.append(CARDS.pop(0))
		choices = A[:]
		drop_ops = valid_moves(choices)
		try:
			strat_dict = strategy[(str(sorted(choices)),str(KNOWNS),HMAID,str(deck))]
		except:
			strat_dict = {}
		perf_dict = prep_perfdict(drop_ops, strat_dict)
		drop = strategy_bandit(perf_dict, arg)
		if drop>10: A.remove(drop/10)
		else:		A.remove(drop)
		if drop == known_B or drop/10 == known_B:
			known_B = 0
		A, B, CARDS, hmaid_A, known_A, known_B, win_flag, xtr_drop = get_action('A', A, B, CARDS, drop, hmaid_B, known_A, known_B)
	
	else:
		B.append(CARDS.pop(0))
		choices = B[:]
		drop_ops = valid_moves(choices)
		shuffle(drop_ops)
		drop = drop_ops[0]
		if drop>10: B.remove(drop/10)
		else:		B.remove(drop)
		if drop == known_A or drop/10 == known_A:
			known_A = 0
		A, B, CARDS, hmaid_B, known_A, known_B, win_flag, xtr_drop = get_action('B', A, B, CARDS, drop, hmaid_A, known_A, known_B)
	
	tmpdrop = drop
	if drop>10: tmpdrop/=10
	SEEN.append(tmpdrop)
	if xtr_drop:
		SEEN.append(xtr_drop)

	return A, B, CARDS, SEEN, hmaid_A, hmaid_B, known_A, known_B, win_flag 


def test_step0(move, A, B, CARDS, SEEN, hmaid_A, hmaid_B, known_A, known_B, strategy, arg="Random"):
	
	choices = None

	deck = Counter(SEEN)
	deck = sorted(deck.items(), key=itemgetter(0))
	
	KNOWNS = (known_A, known_B)
	if move == 'B':
		KNOWNS = (known_B, known_A)
	
	HMAID = hmaid_B
	if move == 'B':
		HMAID = hmaid_A
	
	drop = None

	# implement use of strategy here !!! #TODO
	if move == 'A':
		A.append(CARDS.pop(0))
		choices = A[:]
		drop_ops = valid_moves(choices)
		try:
			strat_dict = strategy[(str(sorted(choices)),str(KNOWNS),HMAID,str(deck))]
		except:
			strat_dict = {}
		perf_dict = prep_perfdict(drop_ops, strat_dict)
		drop = strategy_bandit(perf_dict, arg)
		if drop>10: A.remove(drop/10)
		else:		A.remove(drop)
		if drop == known_B or drop/10 == known_B:
			known_B = 0
		A, B, CARDS, hmaid_A, known_A, known_B, win_flag, xtr_drop = get_action('A', A, B, CARDS, drop, hmaid_B, known_A, known_B)
	
	else:
		B.append(CARDS.pop(0))
		drop_ops = valid_moves(choices)
		shuffle(drop_ops)
		drop = drop_ops[0]
		if drop>10: B.remove(drop/10)
		else:		B.remove(drop)
		if drop == known_A or drop/10 == known_A:
			known_A = 0
		A, B, CARDS, hmaid_B, known_A, known_B, win_flag, xtr_drop = get_action('B', A, B, CARDS, drop, hmaid_A, known_A, known_B)
	
	tmpdrop = drop
	if drop>10: tmpdrop/=10
	SEEN.append(tmpdrop)
	if xtr_drop:
		SEEN.append(xtr_drop)

	return A, B, CARDS, SEEN, hmaid_A, hmaid_B, known_A, known_B, win_flag 


