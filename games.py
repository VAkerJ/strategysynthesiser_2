class Game:
    def __init__(self, L, L0, Sigma, Delta, Obs, noa, name):
        self.L = L
        self.L0 = L0
        self.Sigma = Sigma
        self.Delta = Delta
        self.Obs = Obs
        self.noa = noa
        self.name = name
        return

Games = []

#The Chemical game [0]
#number of agents
noa = 2
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
    ("bad", ("switch", "lift"), "lose"), ("good", ("switch", "lift"), "lose"),
    ("good", ("lift", "switch"), "lose"), ("good", ("lift", "lift"), "win")
]
# observation partitioning
Obs = [
    [...],
    [["bad", "good"], ...]
]
Games.append(Game(L, L0, Sigma, Delta, Obs, noa, "chemical"))

#Supervisor for 2 agents [1]
#number of agents
noa = 2
# states
L = ["start", "one", "two", "three", "win"]
# initial state
L0 = "start"
# action alphabet
Sigma = ("ab", "ab")

# action labeled transitions
Delta = [
    ("start", ..., "start"), ("start", ..., "one"), ("start", ..., "two"),
    ("one", "aa", "one"), ("one", "ab", "one"), ("one", "ba", "one"), ("one", "bb", "three"),
    ("three", "aa", "three"), ("three", "ab", "three"), ("three", "ba", "three"), ("three", "bb", "two"), 
    ("two", "bb", "two"), ("two", "ba", "two"), ("two", "ab", "two"), ("two", "aa", "win"),
    ("win", ..., "win")
]
# observation partitioning
Obs = [
    [["one", "two"], ...],
    [...]
]
Games.append(Game(L, L0, Sigma, Delta, Obs, noa, "supervisor2"))


#Example Game 1 (almost surely winning) [2]
#number of agents
noa = 2
# states
L = ["start", "one", "two", "three", "four", "win", "lose"]
# initial state
L0 = "start"
# action alphabet
Sigma = (("a", "b"), ("a", "b"))

# action labeled transitions
Delta = [
    ("start", ("a", "b"), "start"), ("start", ("b", "a"), "start"), ("start", ("a", "a"), "one"), ("start", ("b", "b"), "two"),
    ("one", ..., "three"),
    ("two", ("a", "a"), "four"), ("two", ("b", "a"), "two"), ("two", ("a", "b"), "two"), ("two", ("b", "b"), "three"),
    ("three", ("a", "a"), "three"), ("three", ("b", "a"), "three"), ("three", ("a", "b"), "lose"), ("three", ("a", "b"), "four"), ("three", ("b", "b"), "three"),
    ("four", ..., "win"),
    ("win", ..., "win")
]
# observation partitioning
Obs = [
    [...],
    [...]
]
Games.append(Game(L, L0, Sigma, Delta, Obs, noa, "example1"))

#Example Game 2 (looping surely winning) [3]
#number of agents
noa = 2
# states
L = ["start", "one", "two", "three", "win"]
# initial state
L0 = "start"
# action alphabet
Sigma = (("a", "b"), ("a", "b"))

# action labeled transitions
Delta = [
    ("start", ("a", "b"), "start"), ("start", ("b", "a"), "start"), ("start", ("b", "b"), "start"), ("start", ("a", "a"), "one"),
    ("one", ..., "two"),
    ("two", ("b", "a"), "two"), ("two", ("a", "b"), "two"), ("two", ("b", "b"), "three"), ("two", ("a", "a"), "win"),
    ("three", ..., "one")
]
# observation partitioning
Obs = [
    [...],
    [...]
]
Games.append(Game(L, L0, Sigma, Delta, Obs, noa, "example2"))

#Cops and robbers [4]
#number of agents
noa = 2
# states
L = ["start", "T1", "T2", "T3", "T4", "win"]
# initial state
L0 = "start"
# action alphabet
Sigma = (("one", "two", "three", "four", "init"), ("one", "two", "three", "four", "init"))
# action labeled transitions
Delta = [
    ("start", ("init", "init"), {"T1", "T2", "T3", "T4"}),
    ("T1", ("one", "one"), "win"), ("T1", ("one", "two"), "win"), ("T1", ("one", "three"), "win"), ("T1", ("one", "four"), "win"), ("T1", ("two", "one"), "win"), ("T1", ("three", "one"), "win"), ("T1", ("four", "one"), "win"),
    ("T1", ("two", "two"), "T2"), ("T1", ("two", "three"), "T2"), ("T1", ("two", "four"), "T2"), ("T1", ("three", "two"), "T2"), ("T1", ("three", "three"), "T2"), ("T1", ("three", "four"), "T2"), ("T1", ("four", "two"), "T2"), ("T1", ("four", "three"), "T2"), ("T1", ("four", "four"), "T2"),
    ("T2", ("two", "two"), "win"), ("T2", ("two", "one"), "win"), ("T2", ("two", "three"), "win"), ("T2", ("two", "four"), "win"), ("T2", ("one", "two"), "win"), ("T2", ("three", "two"), "win"), ("T2", ("four", "two"), "win"),
    ("T2", ("one", "one"), {"T1", "T3"}), ("T2", ("one", "three"), {"T1", "T3"}), ("T2", ("one", "four"), {"T1", "T3"}), ("T2", ("three", "one"), {"T1", "T3"}), ("T2", ("three", "three"), {"T1", "T3"}), ("T2", ("three", "four"), {"T1", "T3"}), ("T2", ("four", "one"), {"T1", "T3"}), ("T2", ("four", "three"), {"T1", "T3"}), ("T2", ("four", "four"), {"T1", "T3"}),
    ("T3", ("three", "three"), "win"), ("T3", ("three", "one"), "win"), ("T3", ("three", "two"), "win"), ("T3", ("three", "four"), "win"), ("T3", ("one", "three"), "win"), ("T3", ("two", "three"), "win"), ("T3", ("four", "three"), "win"),
    ("T3", ("one", "one"), {"T2", "T4"}), ("T3", ("one", "two"), {"T2", "T4"}), ("T3", ("one", "four"), {"T2", "T4"}), ("T3", ("two", "one"), {"T2", "T4"}), ("T3", ("two", "two"), {"T2", "T4"}), ("T3", ("two", "four"), {"T2", "T4"}), ("T3", ("four", "one"), {"T2", "T4"}), ("T3", ("four", "two"), {"T2", "T4"}), ("T3", ("four", "four"), {"T2", "T4"}),
    ("T4", ("four", "four"), "win"), ("T4", ("four", "two"), "win"), ("T4", ("four", "three"), "win"), ("T4", ("four", "one"), "win"), ("T4", ("one", "four"), "win"), ("T4", ("two", "four"), "win"), ("T4", ("three", "four"), "win"),
    ("T4", ("one", "one"), "T3"), ("T4", ("one", "two"), "T3"), ("T4", ("one", "three"), "T3"), ("T4", ("two", "one"), "T3"), ("T4", ("two", "two"), "T3"), ("T4", ("two", "three"), "T3"), ("T4", ("three", "one"), "T3"), ("T4", ("three", "two"), "T3"), ("T4", ("three", "three"), "T3"),
]
# observation partitioning
Obs = [
    [["T1", "T2", "T3", "T4"], ...],
    [["T1", "T2", "T3", "T4"], ...]
]
Games.append(Game(L, L0, Sigma, Delta, Obs, noa, "CopsAndRobbers"))


#Triple agent game [5]
#number of agents
noa = 3

# states
L = ["start", "one", "two", "three", "four", "win", "lose"]

# initial state
L0 = "start"

# action alphabet
Sigma = (("a", "b", "c"), ("a", "b", "c"), ("a", "b", "c"))

# action labeled transitions
Delta = [
    ("start", ("a", "b", "c"), "one"), ("start", ("a", "c", "b"), "one"), 
    ("start", ("b", "a", "c"), "two"), ("start", ("b", "c", "a"), "two"),
    ("start", ("c", "a", "b"), "three"), ("start", ("c", "b", "a"), "three"),
    ("one", ("a", "b", "c"), "lose"), ("one", ("a", "c", "b"), "lose"),
    ("one", ("b", "a", "c"), "one"), ("one", ("c", "b", "a"), "one"),
    ("one", ("b", "c", "a"), "two"), ("one", ("c", "a", "b"), "two"),
    ("two", ("b", "a", "c"), "two"), ("two", ("a", "c", "b"), "two"),
    ("two", ("a", "b", "c"), "two"), ("two", ("b", "c", "a"), "four"),
    ("two", ("c", "a", "b"), "four"), ("two", ("c", "b", "a"), "four"),
    ("three", ("a", "b", "c"), "four"), ("three", ("a", "c", "b"), "four"),
    ("three", ("b", "a", "c"), "four"), ("three", ("b", "c", "a"), "lose"),
    ("three", ("c", "a", "b"), "lose"), ("three", ("c", "b", "a"), "lose"),
    ("four", ("b", "a", "c"), "four"), ("four", ("a", "c", "b"), "win"),
    ("four", ("a", "b", "c"), "four"), ("four", ("b", "c", "a"), "win"),
    ("four", ("c", "a", "b"), "four"), ("four", ("c", "b", "a"), "win")
]

# observation partitioning
Obs = [
    [...],
    [...],
    [["one", "two"], ...]
]
Games.append(Game(L, L0, Sigma, Delta, Obs, noa, "three"))