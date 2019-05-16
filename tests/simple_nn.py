import numpy as np


############################################################################################################
############################################################################################################
class NeuralNetwork:
    ############################################################################################################
    def __init__(self, input_size, hidden_size, output_size, learning_rate, weight_init):

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weight_mean = weight_init[0]
        self.weight_stdev = weight_init[1]

        self.h_bias = np.random.normal(self.weight_mean, self.weight_stdev, [self.hidden_size])
        self.h_x = np.random.normal(self.weight_mean, self.weight_stdev, [self.hidden_size, self.input_size])

        self.o_bias = np.random.normal(self.weight_mean, self.weight_stdev, [self.output_size])
        self.o_h = np.random.normal(self.weight_mean, self.weight_stdev, [self.output_size, self.hidden_size])

        self.learning_rate = learning_rate

    ############################################################################################################
    def feedforward(self, x):
        h = self.tanh(np.dot(self.h_x, x) + self.h_bias)
        o = self.sigmoid(np.dot(self.o_h, h) + self.o_bias)
        return h, o

    ############################################################################################################
    @staticmethod
    def calc_cost(y, o):
        return y - o
        # absolute value of the difference

    ############################################################################################################
    def backpropogation(self, x, o, h, o_cost):
        o_delta = o_cost * self.sigmoid_prime(o)

        h_cost = np.dot(o_delta, self.o_h)
        h_delta = h_cost * self.tanh_prime(h)

        # change all these to -=
        self.o_bias += o_delta * self.learning_rate
        self.o_h += (np.dot(o_delta.reshape(len(o_delta), 1), h.reshape(1, len(h))) * self.learning_rate)

        self.h_bias += h_delta * self.learning_rate
        self.h_x += (np.dot(h_delta.reshape(len(h_delta), 1), x.reshape(1, len(x))) * self.learning_rate)

    ############################################################################################################
    @staticmethod
    def tanh(z):
        return np.tanh(z)

    ############################################################################################################
    @staticmethod
    def tanh_prime(z):
        return 1.0 - np.tanh(z)**2

    ############################################################################################################
    @staticmethod
    def sigmoid(z):
        return 1/(1+np.exp(-z))

    ############################################################################################################
    @staticmethod
    def sigmoid_prime(z):
        return 1/(1+np.exp(-z)) * (1 - 1/(1+np.exp(-z)))


def main():
    x_list = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
    y_list = [[0.0, 0.0, 0.0], [0.0, 1.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 0.0]]

    # and, or, xor

    input_size = 2
    hidden_size = 5
    output_size = 3
    learning_rate = 0.2
    num_epochs = 10000
    weight_init = [0, 0.5]

    net = NeuralNetwork(input_size, hidden_size, output_size, learning_rate, weight_init)

    for i in range(num_epochs):
        epoch_cost = 0
        for j in range(len(x_list)):
            x = np.array(x_list[j], float)
            y = np.array(y_list[j], float)
            h, o = net.feedforward(x)
            o_cost = net.calc_cost(y, o)
            net.backpropogation(x, o, h, o_cost)
            epoch_cost += (o_cost ** 2).sum()
            if i % 100 == 0:
                print("Cost:", epoch_cost)

    for i in range(len(x_list)):
        x = np.array(x_list[i], float)
        y = np.array(y_list[i], float)
        h, o = net.feedforward(x)
        o_cost = net.calc_cost(y, o)
        print("x:", x, " | y:", y, " | o:", '{}'.format(o), " | cost:", '{:0.3f}'.format((o_cost ** 2).sum()))


main()
