#!/usr/bin/env python

from random import shuffle, random
import operator

def strategy_bandit(perfdict, strategy="Random", param = 0.01):
	choices = perfdict.keys()
	if strategy == "eps-greedy" and len(choices):
		rnd = random()
		if rnd > param:
			return max(perfdict.iteritems(), key=operator.itemgetter(1))[0]
		else:
			return strategy_bandit(perfdict, "Random")
	else:
		shuffle(choices)
		return choices[0]


