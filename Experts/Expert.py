class Expert(object):
    """Knowledge source - base class """

    def __init__(self, blackboard, name = "Expert"):
        self.blackboard = blackboard
        self.name = name
        print "Initializing expert: ", self.name

    def precondition(self):
        return True

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)
                   