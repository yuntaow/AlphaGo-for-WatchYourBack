from Coach import Coach
from watch.WatchGame import WatchGame
from watch.keras.NNet import NNetWrapper as nn

from utils import *
args = dotdict({
    'numIters': 10,
    'numEps': 10,
    'tempThreshold': 15,
    'updateThreshold': 0.6,
    'maxlenOfQueue': 20000,
    'numMCTSSims': 60,
    'arenaCompare': 10,
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})

if __name__=="__main__":
    g = WatchGame(n=4,maxi=8)
    nnet = nn(g)

    if args.load_model:
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

    c = Coach(g, nnet, args)
    if args.load_model:
        print("Load trainExamples from file")
        c.loadTrainExamples()
    c.learn()

# if __name__=="__main__":
#     g = TicTacToeGame()
#     nnet = nnn(g)

#     if args.load_model:
#         nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

#     c = Coach(g, nnet, args)
#     if args.load_model:
#         print("Load trainExamples from file")
#         c.loadTrainExamples()
#     c.learn()
 

# if __name__=="__main__":
#     g = OthelloGame(n = 5)
#     nnet = nnnn(g)

#     if args.load_model:
#         nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

#     c = Coach(g, nnet, args)
#     if args.load_model:
#         print("Load trainExamples from file")
#         c.loadTrainExamples()
#     c.learn()