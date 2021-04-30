#!/usr/bin/env python3

from mkbsc import MultiplayerGame, iterate_until_isomorphic, \
                  export, to_string, from_string, to_file, from_file
from stratsynth_2 import Coalition_strat_synth
from games import Games
import os
import sys

nos = 1
method = "b"
if len(sys.argv) > 1:
    Game = Games[int(sys.argv[1])]
    if len(sys.argv) > 2:
        goal = sys.argv[2]
        if len(sys.argv) > 3:
            nos = sys.argv[3]
            if len(sys.argv) > 4: method = sys.argv[4]

else:
    Game = Games[0]

try:
    goal = goal
except:
    goal = "find_one"
#G is a MultiplayerGame-object, and so are GK and GK0
#G = MultiplayerGame.create(Game.L, Game.L0, Game.Sigma, Game.Delta, Game.Obs)
#GK = G.KBSC()
#
#G0 = G.project(0)
#G1 = G.project(1)
#
#GK0 = G0.KBSC()
#GK1 = G1.KBSC()

directory = 'pictures/' + Game.name
if not os.path.exists(directory):
    os.makedirs(directory)
#export the GK game to ./pictures/GK.png

#export(G, "G", view=False, folder = directory)
#export(GK, "GK", view=False, folder = directory)
#
#export(GK0, "GK0", view=False, folder = directory)
#export(GK1, "GK1", view=False, folder = directory)


game = Coalition_strat_synth(gamename=Game.name + "/GK", win_nodes=[("win", "win")], lose_nodes=[("lose", "lose")], start_nodes=[("start", "start")], goal=goal, nr_of_strats=nos, method = method)
#game = Coalition_strat_synth(gamename=Game.name + "/GK", noa=2, win_nodes="{win}", lose_nodes="{lose}", start_nodes="{start}")
game.start_test()
