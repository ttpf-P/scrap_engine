import random


class Neuron:
    def __init__(self):
        self.predecessors = []
        self.value = 0

    def update(self):
        value_new = 0
        length = len(self.predecessors)
        for synapse in range(length):
            value_new += self.predecessors[synapse][0].value * self.predecessors[synapse][1]
        self.value = value_new / length
        del value_new
        del length
        del synapse

    def mutate(self, lr, score):
        for synapse in range(len(self.predecessors)):
            score = (160000 - score**2) / 160000
            if score <= 0:
                print("smth")
                score = 0.000001
            rand = random.uniform(-lr * score, lr * score)
            # print(rand)
            self.predecessors[synapse][1] += rand
            del rand
        del synapse
        del score


class InputNeuron(Neuron):
    def __init__(self):
        super().__init__()
        del self.predecessors

    def update(self):
        pass

    def mutate(self, lr, score):
        pass
