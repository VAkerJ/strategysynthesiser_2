#!/usr/bin/env python3

from mkbsc import MultiplayerGame, iterate_until_isomorphic, \
                  export, to_string, from_string, to_file, from_file
from games import Games
import os
import sys
from ISPLconverter import makeISPL

if len(sys.argv) > 1:
    games = Games[int(sys.argv[1])]
else:
    games = Games

    for game in games:
        print(game.name + ":")

        G = MultiplayerGame.create(game.L, game.L0, game.Sigma, game.Delta, game.Obs)
        GK = G.KBSC()

        GKA = []

        for n in range(game.noa):
            Gtemp = G.project(n)
            GKA.append(Gtemp.KBSC())

        directory = 'pictures/' + game.name
        if not os.path.exists(directory):
            os.makedirs(directory)

        export(G, "G", view=False, folder = directory)
        export(GK, "GK", view=False, folder = directory)

        for idg, gka in enumerate(GKA): export(gka, "GK"+str(idg), view=False, folder = directory)
        print("Expansion done, translating to .ispl")
        makeISPL(game.name)
        print("Translation done\n")

