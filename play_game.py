#!/usr/bin/env python

from collections import defaultdict
import pickle

from utilities import determine_winner, print_deck, score
from game import game_step, game_setup
from test_game import test_game

# game-run counter
games_count = 0
#strategy_scr = pickle.load(open('strategy_record_scr_v0.pkl', 'rb'))
#strategy_tot = pickle.load(open('strategy_record_tot_v0.pkl', 'rb'))
#strategy_loaded = defaultdict(dict)
strategy_loaded = pickle.load(open('strategy/strategy_learned_v0.pkl', 'rb'))
#for state in strategy_scr:
#	choices, KNOWNS, HMAID, deck, drop = state
#	strategy_loaded[(str(choices),str(KNOWNS),HMAID,str(deck))][drop] = strategy_scr[state]/strategy_tot[state]

#del strategy_scr
#del strategy_tot

strategy_record_scr = defaultdict(lambda: 0.5)
strategy_record_tot = defaultdict(lambda: 1)

global PRINT
PRINT = True

while games_count < 10:
    if PRINT: print "*" * 30
    games_count += 1
    CARDS, SEEN, A, B, hmaid_A, hmaid_B, known_A, known_B, win_flag, game_states, cnt = game_setup(
    )
    while True:
        if PRINT: print_deck(A, B, CARDS, SEEN)
        win_flag, br_flag = determine_winner(win_flag, A, B, CARDS, PRINT)
        if br_flag:
            break
        A, B, CARDS, SEEN, hmaid_A, hmaid_B, known_A, known_B, win_flag, decision = game_step(
            ['A', 'B'][cnt % 2], A, B, CARDS, SEEN, hmaid_A, hmaid_B, known_A,
            known_B, PRINT, strategy_loaded)
        game_states.append(decision)
        cnt = 1 - cnt

    for state in game_states:
        move, situation = state[0], tuple(state[1:])
        strategy_record_scr[situation] += score(move, win_flag)
        strategy_record_tot[situation] += 1
    """
	for state in game_states:
		move, choices, KNOWNS, HMAID, deck, drop = state
		situation = tuple(state[1:])
		strategy_loaded[(str(choices),str(KNOWNS),HMAID,str(deck))][drop] = strategy_record_scr[situation]/strategy_record_tot[situation]
	"""

    if games_count % 100000 == 0:
        num_games = 10000.
        scoringA, scoringB = test_game(
            int(num_games), strategy_loaded, "eps-greedy")

        print "=" * 30
        print "after #", games_count, "games..."
        print "length of dict =", len(strategy_loaded.keys())
        print "-" * 20
        print "A is the first player:"
        for win_flag in scoringA:
            print win_flag, scoringA[win_flag] / num_games
        print "-" * 20
        print "B is the first player:"
        for win_flag in scoringB:
            print win_flag, scoringB[win_flag] / num_games

# see strategy sheet after several games
#print '\n','='*20,'\n','strategy_record... '
#for state in strategy_record_scr:
#	print state,":::", strategy_record_scr[state], "of", strategy_record_tot[state], "===", strategy_record_scr[state]/strategy_record_tot[state]

# write pickled object
#pickle.dump(strategy_record_scr, open('strategy_record_scr_v0.pkl', 'wb'))
#pickle.dump(strategy_record_tot, open('strategy_record_tot_v0.pkl', 'wb'))
#pickle.dump(strategy_loaded, open('strategy_learned_v0.pkl', 'wb'))
"""
# test game
num_games = 10000
scoringA, scoringB = test_game(num_games, strategy_loaded, "Random")

# write rand game record
print "-"*20
for win_flag in scoringA:
	print win_flag, scoringA[win_flag]/10000.
print "-"*20
for win_flag in scoringB:
	print win_flag, scoringB[win_flag]/10000.

# test game
num_games = 10000
scoringA, scoringB = test_game(num_games, strategy_loaded, "eps-greedy")

# write rand game record
print "-"*20
for win_flag in scoringA:
	print win_flag, scoringA[win_flag]/10000.
print "-"*20
for win_flag in scoringB:
	print win_flag, scoringB[win_flag]/10000.
"""
