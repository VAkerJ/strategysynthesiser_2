from .graph import *
from copy import deepcopy
from numpy import array
from itertools import product
from .Agent_strat_synth import *

class Coalition_strat_synth():

    def __init__(self, gamename, win_nodes=[("win", "win")], lose_nodes=[("lose", "lose")], start_nodes=[("start", "start")], goal="find_one", nr_of_strats=1, method = "backwards"):
        self.game = None
        self.agent_graphs = None
        self.filename = gamename
        self.win_nodes = win_nodes
        self.lose_nodes = lose_nodes
        self.start_nodes = start_nodes
        self.agents = []
        self.strats = {}

        self.goals = ["find_one", "find_one_sw", "find_all", "find_n"]
        nr_of_strats = int(nr_of_strats)
        try:
            nr_of_strats = int(nr_of_strats)
        except:
            nr_of_strats = 0

        if goal not in self.goals or nr_of_strats < 1:
            print("Invalid goal, using 'find_one'\n")
            goal = "find_one"
            nr_of_strats = 1 
        self.nr_of_strats = nr_of_strats
        self.goal = goal

        self.nr_of_agents = None
        self.done = False
        self.nr_of_w = 0
        self.nr_of_sw = 0

        if method.lower() == "b":
            self.Agent_strat_synth = Backwards_strat_synth
        elif method.lower() == "f":
            self.Agent_strat_synth = Forwards_strat_synth
        elif method.lower() == "bp":
            self.Agent_strat_synth = Backwards_partial_synth
        elif method.lower() == "fp":
            self.Agent_strat_synth = Forwards_partial_synth
        else:
            print("Invalid method, using default")
            self.Agent_strat_synth = Backwards_strat_synth


    def start_test(self):

        test = Game_graph(self.filename)
        test.deltaDic()
        
        self.game = test.get_int_graph()
        self.agent_graphs = test.get_agents()
        self.to_str = test.get_to_str_dict()
        self.nr_of_agents = len(test.agents)

        temp = test.get_to_int_locdict()

        self.win_nodes = self.test_nodes(temp, self.win_nodes, "win_nodes")
        self.lose_nodes = self.test_nodes(temp, self.lose_nodes, "lose_nodes")
        self.start_nodes = self.test_nodes(temp, self.start_nodes, "start_nodes")

        if not(self.win_nodes) or not(self.start_nodes):
            if not(self.win_nodes): print("Insufficient win_nodes")
            if not(self.start_nodes): print("Insufficient start_nodes")
            print("Terminating")
        else:
            self.find_strategy()
            self.print_strats()

    def test_nodes(self, dic, nodes, name):
        remove = []
        for node in nodes:
            for idn, n in enumerate(node):
                if n not in dic[idn]:
                    remove.append(node)

        remove = set(remove)
        if remove: print(str(remove) + " are invalid nodes, removing from '" + name + "'\n")
        nodes = [tuple([dic[idn][n] for idn, n in enumerate(node)]) for node in nodes if node not in remove]
        return nodes


    def find_strategy(self):

        win_n = array(self.win_nodes).T
        lose_n = array(self.lose_nodes).T
        start_n = array(self.start_nodes).T
        if len(lose_n) == 0: lose_n = [[None]]*self.nr_of_agents

        for n in range(self.nr_of_agents):
        
            if self.Agent_strat_synth.is_inv(): graph = self.agent_graphs[n].get_int_inv_graph()
            else: graph = self.agent_graphs[n].get_int_graph()

            new_agent = self.Agent_strat_synth(graph, set(win_n[n]), set(lose_n[n]), set(start_n[n]), n)
            new_agent.generate_main_partial()
            self.agents.append(new_agent)

        if self.goal == self.goals[2]: self.find_all_strats(self.agents) # find all
        else:
            self.test_strats(self.agents[0].partials, 0) #testing strats for agent[0] against all others
            self.find_some_strats(self.agents)
        

    def find_some_strats(self, agents):
        while not self.done:
            for agent in agents:
                partials, empty = agent.generate_new_partials()

                if partials: self.test_strats(partials, agent.id)

                if empty:
                    agents = [a for a in agents if a is not agent]
                    if not(agents): self.done = True
                
                if self.done: break

    def find_all_strats(self, agents):
        for agent in agents:
            empty = agent.is_empty()
            while not empty :
                empty = agent.generate_new_partials()[1]

        self.test_strats()


    def test_strats(self, partials=[], agent_id=-1):
        p_list = [[]]*self.nr_of_agents

        if partials: p_list[agent_id] = partials

        for ida, agent in enumerate(self.agents):
                if ida != agent_id: p_list[ida] = agent.partials

        strats = product(*p_list)
        for strat in strats: self.test_strat(strat)

        return 

    def test_strat(self, strat):
        for start in self.start_nodes:
            won = False
            lost = False

            action = tuple([strat[ids][state] for ids, state in enumerate(start)])
            adjacent = self.game[start].get_adjacent_vert()

            node_queue = [node for node in adjacent if action in self.game[start].get_actions(node)]
            checked = deepcopy(node_queue)
            
            while node_queue:
                node = node_queue.pop().get_id()
                
                if node in self.win_nodes:
                    won = True
                    continue

                try:
                    action = tuple([strat[ids][state] for ids, state in enumerate(node)])
                except:
                    lost = True
                    continue

                if node in self.lose_nodes:
                    lost = True
                    continue

                
                adjacent = [a for a in self.game[node].get_adjacent_vert() if action in self.game[node].get_actions(a)]

                new_adj = [a for a in adjacent if a not in checked]

                if new_adj != adjacent:
                    lost = True

                for n in new_adj:
                    node_queue.append(n)
                    checked.append(n)
            
            if won:
                self.add_strat(start, strat, lost)
                if self.check_criterion(): return
        return

    def add_strat(self, start, strat, lost):
        strat, start = self.translate_strat(strat, start)
        if start not in self.strats: self.strats.update({start : {"surely winning" : [], "winning" : []}})

        if lost:
            self.strats[start]["winning"].append(strat)
            self.nr_of_w += 1

        else:
            self.strats[start]["surely winning"].append(strat)
            self.nr_of_sw += 1


    def translate_strat(self, strat, start):
        strat = tuple([{self.to_str[0][ida][state]:self.to_str[1][ida][action] for state, action in S.items()} for ida, S in enumerate(strat)])
        start = tuple([self.to_str[0][ida][state] for ida, state in enumerate(start)])
        return strat, start


    def print_strats(self): # den här kan nog skrivas om lite bättre
        print("\nNumber of strategies found")
        print("Winning: " + str(self.nr_of_w) + ", Surely Winning: " + str(self.nr_of_sw))
        print("Total: " + str(self.nr_of_w + self.nr_of_sw))
        print("\nFor starting state")
        for start in self.strats.keys():
            print(str(start) + ":")
            categories = self.strats[start].keys()
            for cat in categories:
                cs = self.strats[start][cat]
                if cs != []:
                    print("\n" + cat + ":")
                    for ids, s in enumerate(cs):
                        S = ""
                        for ida, a in enumerate(s):
                            S += "Agent" + str(ida) + ": " + str(a) + " | "
                        print("strat" + str(ids) + ": " + str(S))
            print("-"*200)

    def check_criterion(self):
        if self.goal == self.goals[0] or self.goal == self.goals[3]: #find one or n
            self.done = bool(self.nr_of_w + self.nr_of_sw >= self.nr_of_strats)

        elif self.goal == self.goals[1]: #find one surely winning
            if self.nr_of_sw > 0: self.done = True

        return self.done
