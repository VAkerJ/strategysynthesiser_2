
class Vertex:

    def __init__(self, head_vert):
        """
        Creates a new Vertex object

        :param head_vert: Label on node.
        """
        self.id = head_vert
        self.adjacent_vert_dict = {} # Nodes pointed to by the current node

    def add_adjacent_vert(self, new_vert, action):
        """
        Adds a action-labeled transition to a new node.

        :param new_vert: node that action transitions to.
        :param action: action that transitions
        :return:
        """
        if new_vert in self.adjacent_vert_dict:
            for act in action:
                if act not in self.adjacent_vert_dict[new_vert]:
                    self.adjacent_vert_dict[new_vert].append(act)
        else:
            self.adjacent_vert_dict[new_vert] = action

    def get_id(self):
        """
        :return: current nodes label.
        """
        return self.id

    def get_actions(self, vert):
        """
        Get action that transitions to wanted node.

        :param vert: Node as Vertex object.
        :return: action
        """
        return self.adjacent_vert_dict[vert]

    def get_adjacent_vert(self):
        """
        :return: Node(s) (Vertex object(s)) pointed to by current node.
        """
        return list(self.adjacent_vert_dict.keys())

    def get_adjacent_actions(self):
        return list(self.adjacent_vert_dict.values())