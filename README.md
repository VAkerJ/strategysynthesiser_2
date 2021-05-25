# strategysynthesiser_2
This tool has been created by David Berisha & Viktor Åkerblom Jonsson, to synthesise strategies for multi-agent games of imperfect information against nature that have been undergone an expansion in the form of the multi agent knowledge based subset construction using this MKBSC-tool by Helmer and Nylen, found at https://github.com/helmernylen/mkbsc.

## Important Files
The tool contains the following important files.

### graph.py
The script used to parse the .dot file created by the MKBSC-tool. This script creates the objects, lists, and dictionaries representing the expanded game for the coalition of agents. As well as, from the expanded coalition game, extracting the expanded games for the agents projections of the original coalition game and creating the objects, lists, and dictionaries representing these.

### vertex.py
Script handling the verticies between nodes/states.

### Agent_strat_synth.py
This script contains several classes, where each class is a method/algorithm for generating strategies for an agents game.

### strategy_tester_2.py
This is the main script in the tool which makes use of the other sripts to synthesise winning strategies for games.

## Other files in the repository
We used the following files to help ease our use of the tool.

### games.py
Has a class that creates objects containing the information needed by the MKBSC-tool to create the expanded games. Also creates the games we tested. Running the script creates a list of objects that can be used to create the expanded games on which to run our tool.

### expandGames.py
Running this tool uses the MKBSC-tool to expand the games in games.py. Take note however that this script expects the script found at https://github.com/VAkerJ/ISPLconverter to be included in the same folder.

### main.py
This is the function we primarily used when running our tool, this script expects there to be a games.py file to retrieve games from.

## Tutorial
### Directory placement
The simplest way of running our tool is to make use of the tool by Helmer and Nylen found at https://github.com/helmernylen/mkbsc and place the stratsynth_2 folder in the main folder for the MKBSC-tool.

### Game expansion
Use the MKBSC-tool to expand the game you wish to test. Create a directory named after the game in the MKBSC-tool's 'pictures' directory and save the expanded game there.

### Running the tool
#### Setup
By running
```
game = Coalition_strat_synth(gamename=name + "/GK", win_nodes=win_nodes, lose_nodes=lose_nodes, start_nodes=start_nodes, goal=goal, nr_of_strats=nos, method = method)
```
game = the name of the games directory in pictures.

win_nodes = A list of tuples representing the winning states in the expanded coalition game. Where each element in the tuple is the agents observation-state in that winning state presented in as a string.

lose_nodes = A list of tuples representing the losing states in the expanded coalition game. Where each element in the tuple is the agents observation-state in that losing state presented in as a string.

start_nodes = A list of tuples representing the starting states in the expanded coalition game. Where each element in the tuple is the agents observation-state in that starting state presented in as a string.

goal = the goal to strive for when running the tool. May be 'find_one' if one only wishes to find at least one strategy, 'find_n' if one wishes to find at least 'n' strategies and 'find_all' if one wishes to find as many strategeis as possible.

nos = 'n' number of strategies one wishes to find if "goal = 'find_n'"

method = The method for finding strategies for the agents games. These methods may be 'b' for 'Backwards_strat_synth', 'f' for 'Forwards_strat_synth', 'bp' for 'Backwards_partial_synth' or 'fp' for 'Forwards_partial_synth'

#### Running
When the setup is done, everything can be run using
```
game.start_test()
```

#### Example of main.py
Here is an example of how your main.py could look.

```
#!/usr/bin/env python3

from mkbsc import MultiplayerGame, iterate_until_isomorphic, \
                  export, to_string, from_string, to_file, from_file
from stratsynth_2 import Coalition_strat_synth
import os
import sys

#The Chemical game
name = 'chemical'
#number of agents
noa = 2
#states
L = ["start", "bad", "good", "lose", "win"]
#initial state
L0 = "start"
#action alphabet
Sigma = (("grab", "lift", "switch"), ("grab", "lift", "switch"))
#action labeled transitions
Delta = [
    ("start", ("grab", "grab"), "bad"), ("start", ("grab", "grab"), "good"),
    ("bad", ("switch", "switch"), "good"), ("good", ("switch", "switch"), "good"),
    ("bad", ("lift", "lift"), "lose"), ("bad", ("lift", "switch"), "lose"),
    ("bad", ("switch", "lift"), "lose"), ("good", ("switch", "lift"), "lose"),
    ("good", ("lift", "switch"), "lose"), ("good", ("lift", "lift"), "win")
]
#observation partitioning
Obs = [
    [...],
    [["bad", "good"], ...]
]

#G is a MultiplayerGame-object, and so is GK
G = MultiplayerGame.create(L, L0, Sigma, Delta, Obs)
GK = G.KBSC()

directory = 'pictures/' + name
if not os.path.exists(directory):
    os.makedirs(directory)
    
#export the GK game to ./pictures/GK.png
#export(G, "G", view=False, folder = directory)
export(GK, "GK", view=False, folder = directory)


game = Coalition_strat_synth(gamename=name + "/GK", win_nodes=[("win", "win")], lose_nodes=[("lose", "lose")], start_nodes=[("start", "start")])
game.start_test()
```

Which is then run on the terminal using
```
python3 main.py
```
