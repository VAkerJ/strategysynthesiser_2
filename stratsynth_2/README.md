# Documentation

The project has been commented with Python docstrings, so detailed information about the classes and methods can be found by running `pydoc3 -b` from the project's root folder and opening the `stratsynth` module in the browser. While each method has an explanation of its use and parameters, the code itself is less commented as well as a bit messy in some places.
We used the documentation from the MKBSC-tool as a template.

Below is a quick rundown of some of the important classes and functions in the package. To use them, simply import them into your script with e.g. `from stratsynth import Coalition_strat_synth`.

#### `Coalition_strat_synth`
The most important class in the package. This class lets you find all winning strategies (both almost-surely winning and surely-winning) for games that has been expanded by the MKBSC-tool.
You use it by calling it, with appropriate arguments such as `object_name = Coalition_strat_synth(filename)` if you are testing for two agents and the start, lose and win nodes are called 
 *Start*, *Lose*, *Win*, respectively. `object_name = Coalition_strat_synth(filename, noa, win_nodes, lose_nodes, start_nodes)` where the `noa = number of agents` and `win_/lose_nodes = can be a list of winning or losing nodes` and `start_nodes = start node with a custom name`.

##### `.start_test()`

Runs the synthesiser and prints out the winning strategies.

##### `.setCoalitionNodes()`
Checks if there are multiple winning and losing nodes
and makes sure the coalition can handle them
##### `.tester(current_node)`
Tests the current strategy. `current_node = current state being handled`


##### `.lister(list_nr=0, item=None)`
Populates current_test (current coalition strategy) with Agent strategies, initiates the test, de-populate and keep
going until all strategies has been tested.
`list_nr = which agent's strategy list is being added to the current coalition strategy test`. 
`item = An agent's strategy`

##### `.multi_agent(nr)`
Finds all winning strategies for each agent.
`nr = How many agent's are part of the game`

##### `.cur_strat()`
Used for debugging the lister(). It shows the current strategy being tested.


##### `.show_strats()`
Prints out all winning strategies (almost-surely winning and surely-winning)
or that there are no winning strategies


### `Agent_strat_synth`
This class is used to find each agent's winning strategy. It has to be called with arguments for the game graph, and each of the critical nodes,
e.g. `strategies = Agent_strat_synth(graph_path, "{win}", "{lose}", "{start}")` where `graph_path` is a dictionary of each transition in the game graph.

##### `.start_game()`
Initiates `.traverse_game(current_node)` with `current_node = start_node`

##### `.traverse_game(current_node)`
Traverse the game and finds all winning strategies for the agent. `current_node = The current node for the agent`

# Tutorial
*The tutorial assumes that the reader is familiar with multi-player games of imperfect information*

When synthesising strategy for an already known game, `main.py` will usually look something like the following:

```python
from stratsynth import Coalition_strat_synth

game = Coalition_strat_synth(gamename="GK", noa=2, win_nodes="{win}", lose_nodes="{lose}", start_nodes="{start}")
game.start_test()
```
There are five components to the strategy synthesis method:

- gamename: this is the filename of your game. All agent games should be called gamename#, where # is the agent's number.
- noa: this is the number of agents playing the game, excluding nature.
- win_nodes: the states where the agent's win. This can either be a single state `"{win}"` or a list of states `["{win1}", "{win2}"]`. These nodes are the same for all agents.
- lose_nodes: the states where the agent's lose. This can as well be either a single state `{lose}` or a list of states `["{lose1}", "{lose2}"]`. These nodes are the same for all agents.
- start_nodes: the state where the agent's start. This is a single state and all agents start here.

If the game is not yet known, the main.py file could look like this. First creating the game, expanding it with MKBSC and then synthesising a strategy for it.
```python
from mkbsc import MultiplayerGame, export, iterate_until_isomorphic
from stratsynth import Coalition_strat_synth

"""
Game of robots lifting cans of acid onto a conveyor belt.
"""

# states
L = ["start", "bad", "good", "lose", "win"]
# initial state
L0 = "start"
# action alphabet
Sigma = (("grab", "lift", "switch"), ("grab", "lift", "switch"))
# action labeled transitions
Delta = [
    ("start", ("grab", "grab"), "bad"), ("start", ("grab", "grab"), "good"),
    ("bad", ("switch", "switch"), "good"), ("good", ("switch", "switch"), "good"),
    ("bad", ("lift", "lift"), "lose"), ("bad", ("lift", "switch"), "lose"),
    ("bad", ("switch", "lift"), "lose"), ("bad", ("switch", "lift"), "lose"),
    ("good", ("lift", "switch"), "lose"), ("good", ("lift", "lift"), "win")
]
# observation partitioning
Obs = [
    [["start"], ["bad"], ["good"], ["lose"], ["win"]],
    [["start"], ["bad", "good"], ["lose"], ["win"]]
]

#G is a MultiplayerGame-object
G = MultiplayerGame.create(L, L0, Sigma, Delta, Obs)
GK = G.KBSC() # (G)^K

# takes each agent from game G
G0 = G.project(0)  # (G|0)
G1 = G.project(1)  # (G|1)

# applies the KBSC to each agent's game
GK0 = G0.KBSC()  # (G|0)^K
GK1 = G1.KBSC()  # (G|1)^K


# export the game to ./pictures/
export(G, "G")
export(GK, "GK")

export(GK0, "GK0")
export(GK1, "GK1")


game = Coalition_strat_synth(gamename="GK", noa=2, win_nodes="{win}", lose_nodes="{lose}", start_nodes="{start}")
game.start_test()

#cont below for multiple KBSC-applications
```
If that doesn't get it to a high enough standard you can keep applying the .KBSC() to it until you are satisfied. This would look something like below.


```python
#continuation of the above file example

# takes each agent's game from the expanded game GK
GK0_ = GK.project(0)  # G^K|0
GK1_ = GK.project(1)  # G^K|1


#This would be used for G3K's agents. Something is wonky with the MKBSC
G2K0_ = G2K.project(0)
G2K1_ = G2K.project(1)


G2K0 = GK0_.KBSC()  # (G^K|0)^K
G2K1 = GK1_.KBSC()  # (G^K|1)^K

# export the GK game to ./pictures/GK.png
export(G2K, "G2K")

export(GK0_, "GK0_")
export(GK1_, "GK1_")

export(G2K0, "G2K0")
export(G2K1, "G2K1")

# exporting for G3K's agents. Not used in this iteration.
export(G2K0_, "G2K0")
export(G2K1_, "G2K1")

game = Coalition_strat_synth("G2K", 2, "{win-win}", "{lose-lose}", "{start-start}")
game.start_test()
```


##Advanced tutorial.
If the different agents have individual losing nodes the program could look like this.
````python
from stratsynth import *

filename = "filename"

#finds winning strategies for Agent 0
game_graph = Agent_graph(filename +"0")
game_graph.deltaDic()
graph_paths = game_graph.get_graph()
strategy1 = Agent_strat_synth(graph_paths, "{Win}", "{Lose1}", "{Start}")

#finds winning strategies for Agent 0
game_graph = Agent_graph(filename +"1")
game_graph.deltaDic()
graph_paths = game_graph.get_graph()
strategy2 = Agent_strat_synth(graph_paths, "{Win}", "{Lose2}", "{Start}")


test_game = Coalition_graph(filename)
test_game.deltaDic()
coalition_object = Coalition_strat_synth(filename)
coalition_object.game = test_game.get_graph()
coalition_object.setCoalitionNodes()
coalition_object.agent_strats = [strategy1, strategy2]
coalition_object.lister()
coalition_object.show_strats()
````
Here we are basically running the multi_agent() function for each agent and later running the start_test() from Coalition_strat_synth().