#!/usr/bin/env python

from random import shuffle, randint
from operator import itemgetter
from collections import Counter, defaultdict
import pickle

from get_action import get_action
from utilities import determine_winner, print_deck, score
from game import game_step, test_step, game_setup

def test_game(num, strategy, arg):
	# initialize scoring defdict
	scoringA = defaultdict(int)
	scoringB = defaultdict(int)

	while num > 0:
		num -= 1
		# learned program is player "A" and goes first
		CARDS, SEEN, A, B, hmaid_A, hmaid_B, known_A, known_B, win_flag, game_states, cnt = game_setup()
		while True:
			win_flag, br_flag = determine_winner(win_flag, A, B, CARDS, False)
			if br_flag: break
			A, B, CARDS, SEEN, hmaid_A, hmaid_B, known_A, known_B, win_flag  = test_step(['A','B'][cnt%2], A, B, CARDS, SEEN, hmaid_A, hmaid_B, known_A, known_B, strategy, arg)
			cnt = 1 - cnt

		scoringA[win_flag] += 1
		
		# learned program is player "A" but goes second
		CARDS, SEEN, A, B, hmaid_A, hmaid_B, known_A, known_B, win_flag, game_states, cnt = game_setup()
		cnt = 1
		while True:
			win_flag, br_flag = determine_winner(win_flag, A, B, CARDS, False)
			if br_flag: break
			A, B, CARDS, SEEN, hmaid_A, hmaid_B, known_A, known_B, win_flag  = test_step(['A','B'][cnt%2], A, B, CARDS, SEEN, hmaid_A, hmaid_B, known_A, known_B, strategy, arg)
			cnt = 1 - cnt
	
		scoringB[win_flag] += 1

	return scoringA, scoringB

