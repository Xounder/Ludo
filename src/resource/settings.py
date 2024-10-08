# Dimensões da tela e tamanho dos tiles
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480
TILE_SIZE = 32

# Configurações dos passos das peças e limites
PIECE_STEPS_GOAL = 51 
MAX_PIECE_STEPS = 57
MAX_STEPS_MAP = 52

# Maior valor do dado
MAX_DICE_VALUE = 6

# Identificadores para jogadores
PLAYER = 0
AI = 1
INACTIVE = 2

player_status = ['PLAYER', 'AI', '']

# Cores disponíveis para os jogadores
colors = ['yellow', 'blue', 'red', 'green']

# Posições iniciais das peças no lobby para cada cor
lobby_pos = {
    'yellow': [[10, 10], [13, 10], [10, 13], [13, 13]],
    'blue': [[1, 10], [4, 10], [1, 13], [4, 13]],
    'red': [[1, 1], [4, 1], [1, 4], [4, 4]],
    'green': [[10, 1], [13, 1], [10, 4], [13, 4]]
}

# Posições das etapas finais para cada cor
map_goal_steps =  {
    'yellow': [[13, 7], [12, 7], [11, 7], [10, 7], [9, 7], [8, 7]],
    'blue': [[7, 13], [7, 12], [7, 11], [7, 10], [7, 9], [7, 8]],
    'red': [[1, 7], [2, 7], [3, 7], [4, 7], [5, 7], [6, 7]],
    'green': [[7, 1], [7, 2], [7, 3], [7, 4], [7, 5], [7, 6]]
}

# Valores de verificação para cada cor
check_color = {
    'yellow':[-1, 1, 101, 102, 103, 104, 105, 106],
    'blue':[-2, 14, 201, 202, 203, 204, 205, 206],
    'red':[-3, 27, 301, 302, 303, 304, 305, 306],
    'green':[-4, 40, 401, 402, 403, 404, 405, 406],
}

# MAP
# Posições especiais no mapa que possuem estrelas
star_cells = [[8, 12], [2, 8], [6, 2], [12, 6]]

# Células especiais no mapa que possuem estrelas
star_steps = [9, 22, 35, 48]

# Células iniciais no mapa para cada cor
map_fcell = {'yellow': 0, 'blue': 13, 'red': 26, 'green': 39} 

# Posições iniciais no mapa para cada cor
map_fcell_colors = [[13, 8], [6, 13], [1, 6], [8, 1]]

# Ordem dos passos no mapa
map_steps = [[13, 8], [12, 8], [11, 8], [10, 8], [9, 8], [8, 9], [8, 10], [8, 11], [8, 12], [8, 13], [8, 14], [7, 14], 
             [6, 14], [6, 13], [6, 12], [6, 11], [6, 10], [6, 9], [5, 8], [4, 8], [3, 8], [2, 8], [1, 8], [0, 8], [0, 7], 
             [0, 6], [1, 6], [2, 6], [3, 6], [4, 6], [5, 6], [6, 5], [6, 4], [6, 3], [6, 2], [6, 1], [6, 0], [7, 0], [8, 0], 
             [8, 1], [8, 2], [8, 3], [8, 4], [8, 5], [9, 6], [10, 6], [11, 6], [12, 6], [13, 6], [14, 6], [14, 7], [14, 8]]

# Mapa do tabuleiro Ludo
ludo_map = [[-3,  -3,  -3,  -3,  -3,  -3,  37,  38,  39,  -4,  -4,  -4,  -4,  -4, -4],
            [-3,   0,   0,   0,   0,  -3,  36, 401,  40,  -4,   0,   0,   0,   0, -4],
            [-3,   0,   0,   0,   0,  -3,  35, 402,  41,  -4,   0,   0,   0,   0, -4],
            [-3,   0,   0,   0,   0,  -3,  34, 403,  42,  -4,   0,   0,   0,   0, -4],
            [-3,   0,   0,   0,   0,  -3,  33, 404,  43,  -4,   0,   0,   0,   0, -4],
            [-3,  -3,  -3,  -3,  -3,  -3,  32, 405,  44,  -4,  -4,  -4,  -4,  -4, -4],
            [26,  27,  28,  29,  30,  31, -10, 406, -10,  45,  46,  47,  48,  49, 50],
            [25, 301, 302, 303, 304, 305, 306, -10, 106, 105, 104, 103, 102, 101, 51],
            [24,  23,  22,  21,  20,  19, -10, 206, -10,   5,   4,   3,   2,   1, 52],
            [-2,  -2,  -2,  -2,  -2,  -2,  18, 205,   6,  -1,  -1,  -1,  -1,  -1, -1],
            [-2,   0,   0,   0,   0,  -2,  17, 204,   7,  -1,   0,   0,   0,   0, -1],
            [-2,   0,   0,   0,   0,  -2,  16, 203,   8,  -1,   0,   0,   0,   0, -1],
            [-2,   0,   0,   0,   0,  -2,  15, 202,   9,  -1,   0,   0,   0,   0, -1],
            [-2,   0,   0,   0,   0,  -2,  14, 201,   10, -1,   0,   0,   0,   0, -1],
            [-2,  -2,  -2,  -2,  -2,  -2,  13,  12,   11, -1,  -1,  -1,  -1,  -1, -1]]
