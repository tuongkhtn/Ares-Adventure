# from algorithms import printHello
from utils import PriorityQueue

if __name__ == '__main__':
    posAndWeightStones = [(1, 2, 3), (3, 4, 5)]
    nextStone = (3, 4)
    posStones = [x[:2] for x in posAndWeightStones]
    
    index = posStones.index(nextStone)
    
    posAndWeightStones.append((5, 6, posAndWeightStones[index][-1]))
    posAndWeightStones.pop(index)

    print(posAndWeightStones)
    