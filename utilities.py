#!/usr/bin/env python

def determine_winner(win_flag, A, B, CARDS, PRINT):
	if win_flag in ("A", "B"):
		if PRINT: print win_flag, "is the winner"
		return win_flag, True
	elif win_flag == "Draw":
		if PRINT: print "Game was a Draw"
		return win_flag, True
	elif len(CARDS)<=1:
		if A>B:
			win_flag = "A" 
			if PRINT: print "A is the winner"
		elif B>A:
			win_flag = "B"
			if PRINT: print "B is the winner"
		else:
			win_flag = "Draw"
			if PRINT: print "Game was a Draw"
		return win_flag, True
	else:
		return win_flag, False


def print_deck(A, B, CARDS, SEEN):
	print "A: ", A
	print "B: ", B
	print "CARDS: ", CARDS
	print "SEEN: ", SEEN
	print "-"*20	


def score(move, win_flag):
	if move == win_flag:
		return 1
	elif move != win_flag and win_flag != "Draw":
		return 0
	else:
		return 0.5


def drop_options(pick):
	if pick == 1:
		return range(12,19)
	elif pick == 5:
		return range(50,52)
	else:
		return [pick]


def valid_moves(choices):
	if 8 in choices:
		choices.remove(8)
	if sorted(choices)==[5,7] or sorted(choices)==[6,7]:
		return [7]
	drop_ops = []
	for choice in choices:
		drop_ops += drop_options(choice)
	return drop_ops


def prep_perfdict(drop_ops, strategy_dict):
	perf_dict = {}
	for choice in drop_ops:
		perf_dict[choice] = 0
		if choice in strategy_dict:
			perf_dict[choice] = strategy_dict[choice]
	return perf_dict

