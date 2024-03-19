import asyncio
import keyboard

# Função lambda para mover o jogador ou caixa
move = lambda pos, delta: (pos[0] + delta[0], pos[1] + delta[1])

# Função de continuação para verificar se uma posição é válida
is_valid = lambda pos, level: level[pos[0]][pos[1]] != '#'

# Função de alta ordem para verificar se uma posição é um ponto de destino
is_goal = lambda level: lambda pos: level[pos[0]][pos[1]] == '.'

# Closure para verificar se uma posição contém uma caixa
def is_box(level):
    def _is_box(pos):
        return level[pos[0]][pos[1]] == '$'
    return _is_box

# Closure para verificar se uma posição está livre
def is_free(level):
    def _is_free(pos):
        return level[pos[0]][pos[1]] in [' ', '.', '@']
    return _is_free

# Função principal do jogo
async def sokoban(file_path):
    # Lê o arquivo do nível
    with open(file_path, 'r') as file:
        level = [list(line.strip()) for line in file]

    player_pos = None
    boxes = set()
    goals = set()

    # Encontra a posição inicial do jogador, das caixas e dos pontos
    for i, row in enumerate(level):
        for j, char in enumerate(row):
            if char == '@':
                player_pos = (i, j)
            elif char == '$':
                boxes.add((i, j))
            elif char == '.':
                goals.add((i, j))

    # Função para imprimir o nível
    def print_level():
        for row in level:
            print(''.join(row))

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

            if is_valid(new_player_pos, level):
                # Verifica se há uma caixa na nova posição do jogador
                if new_player_pos in boxes:
                    new_box_pos = move(new_player_pos, delta)

                    if is_valid(new_box_pos, level) and new_box_pos not in boxes:
                        boxes.remove(new_player_pos)
                        boxes.add(new_box_pos)

                    level[new_player_pos[0]][new_player_pos[1]] = ' '
                    level[new_box_pos[0]][new_box_pos[1]] = '$'

                level[player_pos[0]][player_pos[1]] = ' '
                player_pos = new_player_pos
                level[player_pos[0]][player_pos[1]] = '@'

        # Verifica se o jogo foi concluído
        if not boxes.symmetric_difference(goals):
            print_level()
            print("Parabéns, você venceu!")
            break

if __name__ == "__main__":
    asyncio.run(sokoban("mapa.txt"))
