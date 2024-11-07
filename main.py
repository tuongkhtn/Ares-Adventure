from utils.GameObject import GameObject
from utils.GameGraphic import GameGraphic

if __name__ == '__main__':    
    gameObject = GameObject("input-01.txt")
    
    gameGraphic = GameGraphic(gameObject)
    gameGraphic.run()