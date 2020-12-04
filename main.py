import neurons
import random
import copy
import logging
logger = logging.Logger("ai")
handler = logging.FileHandler("ai.log")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class NeuralNetwork:
    def __init__(self, structure, lr=0.05):
        self.network = self.generate(structure)
        self.lr = lr

    def generate(self, structure):
        a = 0
        network = [[]]
        for i in range(structure[0]):
            network[0].append(neurons.InputNeuron())
        for i in structure[1]:
            network.append([])
            a += 1
            for x in range(i):
                network[a].append(neurons.Neuron())
                for neuron in network[a-1]:
                    network[a][x].predecessors.append([neuron, random.uniform(-1,1)])
        #network[1][0].predecessors = [[network[0][0], 1]]
        return network

    def run(self):
        for layer in self.network:
            for neuron in layer:
                neuron.update()

    def mutate(self, score=1):
        for layer in self.network:
            for neuron in layer:
                neuron.mutate(self.lr, score)

    def __lt__(self, other):
        return True


class NetworkBatch:
    def __init__(self, structure, lr, gen_size):
        self.networks = []
        for _ in range(gen_size):
            print("gen")
            self.networks.append(NeuralNetwork(structure, lr))
        self.lr = lr
        self.gen_size = gen_size
        self.best = None

    def train(self, score_func, generations):
        for gen in range(generations):
            scores = []
            for network in self.networks:
                scores.append((score_func(network), network))
            scores.sort()
            networks_new = []
            scores_cut = scores[:3]
            for i in range(self.gen_size):
                chosen = random.choice(scores_cut)
                networks_new.append(copy.deepcopy(chosen[1]))
                # networks_new[i].mutate(chosen[0])
                networks_new[i].mutate()
            del self.networks
            self.networks = networks_new
            if gen % 100 == 0:
                logger.info(str(scores[0][0]) + "\t" + str(scores[-1][0]))
            else:
                logger.debug(str(scores[0][0]) + "\t" + str(scores[-1][0]))
            del networks_new
            self.best = scores[0][1]
            del scores


if __name__ == "__main__":
    """NN = NeuralNetwork(())
    NN.run()
    print(NN.network[1][0].value)
    NN.mutate()
    NN.run()
    print(NN.network[1][0].value)"""

    def score_func(network: NeuralNetwork):
        network.network[0][0].value = 1
        network.run()
        return abs(network.network[-1][0].value)

    NB = NetworkBatch((1,[1]), 0.0001, 200)
    NB.train(score_func, 20000)
