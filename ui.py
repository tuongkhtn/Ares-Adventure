import pygame
import sys
import numpy as np
import threading
import time
from algorithms.astar import aStarSearch
from algorithms.dfs import depthFirstSearch
from algorithms.bfs import breadthFirstSearch
from algorithms.ucs import uniformCostSearch
from utils import transferToGameState

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sokoban - Ares and Stones")

# file name
FILE_NAME = "input-01.txt"

# Kích thước ô
TILE_SIZE = 40

# Offset
OFFSET_X = 40
OFFSET_Y = 80

# Biến tốc độ di chuyển
MOVE_SPEED = 5  # pixel per frame

# Màu sắc
COLOR_BG = (230, 241, 216)# Màu nền xanh da trời nhạt
COLOR_WALL = (139, 69, 19)  # Màu tường nâu

# Các biến lưu vị trí Ares, Stones và Switches
level = []
player_pos = []
stones = []
switches = []
stones_weights = []

# Lưu trạng thái trò chơi để quay lại
history = []

# Đếm bước đi và tổng trọng số
steps = 0
total_weight = 0

# Tạo font để hiển thị trọng số và số bước
font = pygame.font.Font(None, 24)
stats_font = pygame.font.Font(None, 36)

# Tải ảnh Ares và đá
ares_image = pygame.image.load('img/ares.png').convert_alpha()
ares_image = pygame.transform.scale(ares_image, (TILE_SIZE, TILE_SIZE))
stone_image = pygame.image.load('img/stone.png').convert_alpha()
stone_image = pygame.transform.scale(stone_image, (TILE_SIZE, TILE_SIZE))
switch_image = pygame.image.load('img/switch.png').convert_alpha()
switch_image = pygame.transform.scale(switch_image, (TILE_SIZE, TILE_SIZE))
freespace_image = pygame.image.load('img/freespace.png').convert_alpha()
freespace_image = pygame.transform.scale(freespace_image, (TILE_SIZE, TILE_SIZE))
wall_image = pygame.image.load('img/wall.png').convert_alpha()
wall_image = pygame.transform.scale(wall_image, (TILE_SIZE, TILE_SIZE))
wall3d_image = pygame.image.load('img/wall3d.png').convert_alpha()
wall3d_image = pygame.transform.scale(wall3d_image, (TILE_SIZE, TILE_SIZE * 1.25))

# Hàm đọc lưới trò chơi và khởi tạo các đối tượng từ file
def load_level_from_file(filename):
    global level, player_pos, stones, switches, stones_weights
    with open(filename, 'r') as f:
        # Đọc dòng đầu tiên lấy trọng số cho từng "stone"
        stones_weights = list(map(int, f.readline().strip().split()))
        
        # Đọc phần còn lại lấy bản đồ trò chơi
        level = [line.rstrip() for line in f.readlines() if line.strip()]  # Loại bỏ dòng trống
        
    # Khởi tạo các đối tượng dựa trên bản đồ
    stone_index = 0
    for row_idx, row in enumerate(level):
        for col_idx, tile in enumerate(row):
            if tile == "@":  # Ares
                player_pos = [row_idx, col_idx]
            elif tile == "$":  # Stone
                stones.append({"pos": [row_idx, col_idx], "weight": stones_weights[stone_index], "screen_pos": [col_idx * TILE_SIZE, row_idx * TILE_SIZE]})
                stone_index += 1
            elif tile == ".":  # Switch
                switches.append([row_idx, col_idx])
            elif tile == "*":  # Stone on Switch
                stones.append({"pos": [row_idx, col_idx], "weight": stones_weights[stone_index], "screen_pos": [col_idx * TILE_SIZE, row_idx * TILE_SIZE]})
                switches.append([row_idx, col_idx])
                stone_index += 1
            elif tile == "+":  # Ares on Switch
                player_pos = [row_idx, col_idx]
                switches.append([row_idx, col_idx])

# Gọi hàm để tải dữ liệu từ file "level.txt"
load_level_from_file(FILE_NAME)

# Vị trí hiển thị ban đầu của Ares
player_screen_pos = [player_pos[1] * TILE_SIZE + OFFSET_X, player_pos[0] * TILE_SIZE + OFFSET_Y]

# Hàm vẽ lưới
def draw_grid():
    for row_idx, row in enumerate(level):
        is_start = True
        for col_idx, tile in enumerate(row):
            if tile != " " or (tile==" " and not is_start):
                is_start = False
                x = col_idx * TILE_SIZE + OFFSET_X
                y = row_idx * TILE_SIZE + OFFSET_Y
                if [row_idx, col_idx] in switches:
                    screen.blit(switch_image, (x, y))
                else:
                    screen.blit(freespace_image, (x, y))

    
    max_length = max(len(sublist) for sublist in level)
    padded_level = [sublist + " " * (max_length - len(sublist)) for sublist in level]

    for col_idx in range(max_length):
        is_start = True
        for row_idx in range(len(padded_level)):
            if padded_level[row_idx][col_idx] == " " and is_start:
                screen.fill(COLOR_BG, (col_idx * TILE_SIZE + OFFSET_X, row_idx * TILE_SIZE + OFFSET_Y, TILE_SIZE, TILE_SIZE))
            else:
                is_start = False

    for col_idx in range(max_length):
        is_start = True
        for row_idx in range(len(padded_level)-1, -1, -1):
            if padded_level[row_idx][col_idx] == " " and is_start:
                screen.fill(COLOR_BG, (col_idx * TILE_SIZE + OFFSET_X, row_idx * TILE_SIZE + OFFSET_Y, TILE_SIZE, TILE_SIZE))
            else:
                is_start = False
                

    
    
    # Vẽ Ares và Stones
    screen.blit(ares_image, (player_screen_pos[0] + OFFSET_X, player_screen_pos[1] + OFFSET_Y))
    for stone in stones:
        screen.blit(stone_image, (stone["screen_pos"][0] + OFFSET_X, stone["screen_pos"][1] + OFFSET_Y))
        weight_text = font.render(str(stone["weight"]), True, (0, 0, 0))
        weight_text_rect = weight_text.get_rect(center=(stone["screen_pos"][0] + TILE_SIZE // 2 + OFFSET_X, stone["screen_pos"][1] + TILE_SIZE // 2 + OFFSET_Y))
        screen.blit(weight_text, weight_text_rect)

    # Vẽ các bức tường sau cùng để chúng "đè" lên các vật thể khác
    for row_idx, row in enumerate(level):
        for col_idx, tile in enumerate(row):
            x = col_idx * TILE_SIZE + OFFSET_X
            y = row_idx * TILE_SIZE + OFFSET_Y
            if tile == "#":
                if row_idx == len(level) - 1 or row_idx == 0 or col_idx == len(row) - 1 or col_idx == 0 or len(row) > len(level[row_idx + 1]) or level[row_idx + 1][col_idx] != "#":
                    screen.blit(wall3d_image, (x, y - 0.25 * TILE_SIZE))
                else:
                    screen.blit(wall_image, (x, y - 0.25 * TILE_SIZE))

# Hàm di chuyển Ares và đẩy đá
def move_ares(dx, dy):
    global player_pos, stones, history, steps, total_weight
    new_x = player_pos[1] + dx
    new_y = player_pos[0] + dy

    # Kiểm tra tường
    if level[new_y][new_x] == "#":
        return

    # Lưu trạng thái hiện tại vào lịch sử, bao gồm cả total_weight
    history.append((player_pos.copy(), [s["pos"].copy() for s in stones], total_weight))
    

    # Kiểm tra nếu Ares đẩy một Stone
    
    for stone in stones:
        if stone["pos"] == [new_y, new_x]:
            stone_new_x = new_x + dx
            stone_new_y = new_y + dy
            # Kiểm tra nếu vị trí mới của Stone hợp lệ (không là tường hay Stone khác)
            if level[stone_new_y][stone_new_x] != "#" and all(s["pos"] != [stone_new_y, stone_new_x] for s in stones):
                # Di chuyển Stone và cộng thêm trọng số
                stone["pos"] = [stone_new_y, stone_new_x]
                total_weight += stone["weight"]  # Cộng trọng số của hòn đá vào tổng trọng số
            else:
                history.pop()  # Nếu không thể di chuyển Stone, xóa trạng thái vừa lưu trong lịch sử
                return  # Nếu không thể di chuyển Stone, dừng lại

    # Di chuyển Ares
    player_pos = [new_y, new_x]
    steps += 1  # Tăng số bước đi

# Hàm di chuyển trượt cho các đối tượng
def interpolate_positions():
    # Di chuyển Ares từ từ đến vị trí mới
    target_x = player_pos[1] * TILE_SIZE
    target_y = player_pos[0] * TILE_SIZE
    if player_screen_pos[0] < target_x:
        player_screen_pos[0] += min(MOVE_SPEED, target_x - player_screen_pos[0])
    elif player_screen_pos[0] > target_x:
        player_screen_pos[0] -= min(MOVE_SPEED, player_screen_pos[0] - target_x)
    if player_screen_pos[1] < target_y:
        player_screen_pos[1] += min(MOVE_SPEED, target_y - player_screen_pos[1])
    elif player_screen_pos[1] > target_y:
        player_screen_pos[1] -= min(MOVE_SPEED, player_screen_pos[1] - target_y)

    # Di chuyển các Stones từ từ đến vị trí mới
    for stone in stones:
        target_x = stone["pos"][1] * TILE_SIZE
        target_y = stone["pos"][0] * TILE_SIZE
        if stone["screen_pos"][0] < target_x:
            stone["screen_pos"][0] += min(MOVE_SPEED, target_x - stone["screen_pos"][0])
        elif stone["screen_pos"][0] > target_x:
            stone["screen_pos"][0] -= min(MOVE_SPEED, stone["screen_pos"][0] - target_x)
        if stone["screen_pos"][1] < target_y:
            stone["screen_pos"][1] += min(MOVE_SPEED, target_y - stone["screen_pos"][1])
        elif stone["screen_pos"][1] > target_y:
            stone["screen_pos"][1] -= min(MOVE_SPEED, stone["screen_pos"][1] - target_y)

# Hàm reset trò chơi
def reset_game():
    global player_pos, stones, switches, history, steps, total_weight
    # Tải lại bản đồ trò chơi từ file gốc
    player_pos = []
    stones = []
    switches = []
    load_level_from_file(FILE_NAME)
    # Đặt lại lịch sử, số bước và tổng trọng số
    history = []
    steps = 0
    total_weight = 0

def back_step():
    global player_pos, stones, history, steps, total_weight
    if history:
        # Lấy trạng thái cuối cùng trong lịch sử
        player_pos, stone_positions, prev_total_weight = history.pop()
        # Đặt lại vị trí của các Stones
        for i, pos in enumerate(stone_positions):
            stones[i]["pos"] = pos
        # Đặt lại tổng trọng số và giảm bước đi
        total_weight = prev_total_weight
        steps = max(0, steps - 1)

# Hàm vẽ nút
def draw_button(text, rect, color):
    text_surface = stats_font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    pygame.draw.rect(screen, color, rect)  # Vẽ nút
    screen.blit(text_surface, text_rect)




# Vòng lặp trò chơi
clock = pygame.time.Clock()
running = True
movement_delay = 100
last_move_time = pygame.time.get_ticks()
algorithm_running = False



    


selected_algorithm = None  # None, "DFS", "BFS", "UCS", "A*"

# Tạo danh sách các thuật toán và chỉ số cho thuật toán hiện tại
algorithms = ["DFS", "BFS", "UCS", "A*"]
search_functions = {
    "DFS": depthFirstSearch,
    "BFS": breadthFirstSearch,
    "UCS": uniformCostSearch,
    "A*": aStarSearch
}
current_algorithm_index = 0  # Bắt đầu với thuật toán đầu tiên
show_algorithm_list = False
# Hàm vẽ nút toggle chọn thuật toán
def draw_toggle_algorithm_button(label, rect, color):
    draw_button(label, rect, color)

# Hàm vẽ danh sách các thuật toán khi mở toggle (hiển thị phía trên)
def draw_algorithm_list():
    for i, algorithm in enumerate(algorithms):
        # Đặt vị trí các nút lên phía trên của toggle
        option_rect = pygame.Rect(algorithm_toggle_button.x, algorithm_toggle_button.y - (i + 1) * 40, 80, 40)
        color =  (128, 128, 128) if i == current_algorithm_index else (200, 200, 200)
        draw_button(algorithm, option_rect, color)

def run_with_ai_search(algorithm):
    global stones_weights, level, algorithm_running
    gameState = transferToGameState(weights=stones_weights, maze=level)
    
    finalNumberOfSteps, finalWeight, numberOfNodes, finalPath, finalStates = algorithm(gameState)
    algorithm_running = True
    for step in finalPath: 
        if algorithm_running == False:
            return
        if step.lower() == "u":  
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
            pygame.event.post(event) 
        elif step.lower() == "d": 
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
            pygame.event.post(event)  
        elif step.lower() == "l": 
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
            pygame.event.post(event) 
        elif step.lower() == "r": 
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
            pygame.event.post(event)
        
        
        time.sleep(0.3) 


while running:
    screen.fill(COLOR_BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            algorithm_running = False
        elif event.type == pygame.KEYDOWN:
            if pygame.time.get_ticks() - last_move_time > movement_delay:
                last_move_time = pygame.time.get_ticks()
                if event.key == pygame.K_UP:
                    move_ares(0, -1)
                elif event.key == pygame.K_DOWN:
                    move_ares(0, 1)
                elif event.key == pygame.K_LEFT:
                    move_ares(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    move_ares(1, 0)
        
        

        # Xử lý nhấn nút bằng chuột
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if reset_button.collidepoint(mouse_pos):
                reset_game()
                algorithm_running = False

            elif back_button.collidepoint(mouse_pos):
                back_step()
            elif play_button.collidepoint(mouse_pos):
                reset_game()
                algorithm = algorithms[current_algorithm_index]
                search_function = search_functions[algorithm]
                astar_thread = threading.Thread(target=run_with_ai_search, args=([search_function]))
                astar_thread.start()

            elif algorithm_toggle_button.collidepoint(mouse_pos):
                show_algorithm_list = not show_algorithm_list  # Mở/đóng danh sách khi nhấn nút toggle
            elif show_algorithm_list:
                # Kiểm tra nhấp vào từng thuật toán trong danh sách
                for i, algorithm in enumerate(algorithms):
                    option_rect = pygame.Rect(algorithm_toggle_button.x, algorithm_toggle_button.y - (i + 1) * 40, 80, 40)
                    if option_rect.collidepoint(mouse_pos):
                        current_algorithm_index = i  
                        show_algorithm_list = False  


    # Nội suy các vị trí của Ares và Stones
    interpolate_positions()
    # Vẽ lưới và các đối tượng
    draw_grid()

    # Vẽ nút Reset
    reset_button = pygame.Rect((WINDOW_WIDTH // 5 - 40), (WINDOW_HEIGHT // 10 * 9), 80, 40)
    draw_button("Reset", reset_button, (0, 0, 255))
    
    # Vẽ nút Back
    back_button = pygame.Rect((WINDOW_WIDTH // 5 * 2 - 40), (WINDOW_HEIGHT // 10 * 9), 80, 40)
    draw_button("Back", back_button, (255, 0, 0))

    # Vẽ nút play
    play_button = pygame.Rect((WINDOW_WIDTH // 5 * 3 - 40), (WINDOW_HEIGHT // 10 * 9), 80, 40)
    draw_button("Play", play_button, (0, 0, 255))

    # Vẽ nút toggle chọn thuật toán
    algorithm_toggle_button = pygame.Rect((WINDOW_WIDTH // 5 * 3 - 40), (WINDOW_HEIGHT // 10 * 9 - 50), 80, 40)
    current_algorithm = algorithms[current_algorithm_index]
    draw_toggle_algorithm_button(current_algorithm, algorithm_toggle_button, (0, 200, 0))

    # Hiển thị danh sách thuật toán nếu toggle được mở
    if show_algorithm_list:
        draw_algorithm_list()

    # Vẽ nút pause
    pause_button = pygame.Rect((WINDOW_WIDTH // 5 * 4 - 40), (WINDOW_HEIGHT // 10 * 9), 80, 40)
    draw_button("Pause", pause_button, (255, 0, 0))

    # Hiển thị số bước đi ở góc trên bên trái và tổng trọng số ở góc trên bên phải
    steps_text = stats_font.render(f"Step Count: {steps}", True, (0, 0, 0))
    weight_text = stats_font.render(f"Weight: {total_weight}", True, (0, 0, 0))
    screen.blit(steps_text, (10, 10))
    screen.blit(weight_text, (WINDOW_WIDTH - 200, 10))  # Hiển thị ở góc trên bên phải

    pygame.display.update() # Cập nhật màn hình sau khi vẽ
    clock.tick(60)  # Giới hạn FPS của trò chơi

