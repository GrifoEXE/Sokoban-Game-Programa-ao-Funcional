import keyboard
import asyncio

class Result:
    def __init__(self, success, value=None, error=None):
        self.success = success
        self.value = value
        self.error = error

    def bind(self, func):
        if self.success:
            return func(self.value)
        else:
            return Result(False, error=self.error)

# Função lambda para mover o jogador ou caixa
move = lambda pos, delta: (pos[0] + delta[0], pos[1] + delta[1])

# Função de continuação para verificar se uma posição é válida
def is_valid(pos, level):
    if pos[0] < 0 or pos[0] >= len(level) or pos[1] < 0 or pos[1] >= len(level[0]):
        return Result(False, error="Out of bounds")
    return Result(level[pos[0]][pos[1]] != '#')

# Função de alta ordem para verificar se uma posição é um ponto de destino
def is_goal(level):
    return lambda pos: level[pos[0]][pos[1]] == '.'

# Closure para verificar se uma posição contém uma caixa
def is_box(level):
    return lambda pos: level[pos[0]][pos[1]] == '$'

# Closure para verificar se uma posição está livre
def is_free(level):
    return lambda pos: level[pos[0]][pos[1]] in [' ', '.']

# Função principal do jogo
async def sokoban(file_path):
    # Lê o arquivo do nível
    with open(file_path, 'r') as file:
        level = [list(line.strip()) for line in file]

    # Encontra a posição inicial do jogador
    player_pos = next((i, j) for i, row in enumerate(level) for j, char in enumerate(row) if char == '@')

    # Inicializa as posições das caixas e dos objetivos usando List Comprehensions
    boxes = {(i, j) for i, row in enumerate(level) for j, char in enumerate(row) if char == '$'}
    goals = {(i, j) for i, row in enumerate(level) for j, char in enumerate(row) if char == '.'}

    # Função para imprimir o nível usando List Comprehension
    def print_level():
        print('\n'.join(''.join(row) for row in level))

    async def get_key():
        while True:
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_DOWN:
                return event.name

    while True:
        print_level()
        print("Use as setas do teclado para mover o jogador.")
        print("Pressione Q para sair.")

        key = await get_key()

        if key == 'q':
            break

        delta = {'up': (-1, 0), 'left': (0, -1), 'down': (1, 0), 'right': (0, 1)}.get(key)

        if delta is not None:
            new_player_pos = move(player_pos, delta)

            is_valid_move = is_valid(new_player_pos, level)
            if is_valid_move.success:
                if is_box(level)(new_player_pos):
                    new_box_pos = move(new_player_pos, delta)
                    is_valid_box_move = is_valid(new_box_pos, level)
                    if is_valid_box_move.success and not is_box(level)(new_box_pos):
                        boxes.remove(new_player_pos)
                        boxes.add(new_box_pos)
                        level[new_player_pos[0]][new_player_pos[1]] = ' '
                        level[new_box_pos[0]][new_box_pos[1]] = '$'
                    else:
                        continue

                level[player_pos[0]][player_pos[1]] = ' '
                player_pos = new_player_pos
                level[player_pos[0]][player_pos[1]] = '@'

        if not boxes.symmetric_difference(goals):
            print_level()
            print("Parabéns, você venceu!")
            break

if __name__ == "__main__":
    asyncio.run(sokoban("mapa.txt"))
