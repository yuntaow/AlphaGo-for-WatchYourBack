import Arena
from MCTS import MCTS
# from othello.OthelloGame import OthelloGame, display

from watch.WatchGame import *
from watch.WatchGameLogic import *
from watch.WatchGamePlayers import *
from watch.keras.NNet import NNetWrapper as nn
from functools import reduce
import numpy as np
from utils import *
import math

g = WatchGame(n=4,maxi=8)

n1 = nn(g)
n1.load_checkpoint('./temp/','best.pth.tar')
# args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
# mcts1 = MCTS(g, n1, args1)
# n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

test = np.array([
		[2,-1,-1,2],
		[1,0,0,0],
		[0,-1,1,0],
		[2,0,1,2]
		])

from keras import backend as K

test = test[np.newaxis, :, :]

i= 0
ii = 2
print()
print()
print("input at layer {}".format(i))
print(n1.nnet.model.layers[i].input)
print("---------")
print("output at layer {}".format(ii))
get_3rd_layer_output = K.function([n1.nnet.model.layers[i].input],
							[n1.nnet.model.layers[ii].output]
						)
print("name", n1.nnet.model.layers[ii].name)
print(n1.nnet.model.layers[ii])
print(get_3rd_layer_output([test]))
print(get_3rd_layer_output([test])[0].shape)



# reshape

def RESHAPE(x):
	size = x[0].shape[0]
	return [np.array(x.reshape(1,size,size,1)).astype(float)]

def RELU(x):
	return np.maximum(0,x)

def forward(inputs):
    fmap = np.zeros((1, 4, 4, 512))
    for j in range(4):
        for i in range(4):
            fmap[1, j, i, :] = np.sum(inputs[1, j * 3:j * 3 + 512, i * 3:i * 3 + 512, :, np.newaxis] * 512, axis=(1, 2, 3))
    return fmap

print("------")
print(np.array(n1.nnet.model.layers[2].get_config()))
print(np.array(n1.nnet.model.layers[2].get_weights())[0].shape)
import pickle
with open("data.lala", "wb") as f:
	pickle.dump(np.array(n1.nnet.model.layers[2].get_weights())[0], f)
print(np.array(n1.nnet.model.layers[2].get_weights())[0])
# print(RESHAPE(test))
r = []
for i in range(3):
	s = []
	for j in range(3):
		print(np.array(n1.nnet.model.layers[2].get_weights())[0][i][j][0][0])
		s.append(np.array(n1.nnet.model.layers[2].get_weights())[0][i][j][0][0])
	r.append(s)
print(r)

b = RESHAPE(test)

print(b)

def CONV(input):
	pass


exit()