from pathlib import Path

class ImageConfig:
    ROOT = Path(__file__).parent.parent
    IMAGE_ROOT = ROOT / "img"
    
    IMAGE_ARES = IMAGE_ROOT / "ares.png"
    IMAGE_FREE_SPACE = IMAGE_ROOT / "freespace.png"
    IMAGE_STONE = IMAGE_ROOT / "stone.png"
    IMAGE_SWITCH = IMAGE_ROOT / "switch.png"
    IMAGE_WALL = IMAGE_ROOT / "wall.png"