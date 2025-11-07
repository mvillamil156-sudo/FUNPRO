
import math

WIN_COMBINATIONS = [
    (0,1,2), (3,4,5), (6,7,8),  # filas
    (0,3,6), (1,4,7), (2,5,8),  # columnas
    (0,4,8), (2,4,6)            # diagonales
]

def print_board(board):
    
    symbols = [cell if cell != ' ' else str(i+1) for i,cell in enumerate(board)]
    print()
    print(f" {symbols[0]} | {symbols[1]} | {symbols[2]} ")
    print("---+---+---")
    print(f" {symbols[3]} | {symbols[4]} | {symbols[5]} ")
    print("---+---+---")
    print(f" {symbols[6]} | {symbols[7]} | {symbols[8]} ")
    print()

def check_winner(board):
    
    for a,b,c in WIN_COMBINATIONS:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    if ' ' not in board:
        return 'Tie'
    return None

def available_moves(board):
    return [i for i,cell in enumerate(board) if cell == ' ']

def minimax(board, depth, is_maximizing, ai_player, human_player):
    
    winner = check_winner(board)
    if winner == ai_player:
        return 10 - depth
    elif winner == human_player:
        return -10 + depth
    elif winner == 'Tie':
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in available_moves(board):
            board[move] = ai_player
            score = minimax(board, depth+1, False, ai_player, human_player)
            board[move] = ' '
            if score > best_score:
                best_score = score
        return best_score
    else:
        best_score = math.inf
        for move in available_moves(board):
            board[move] = human_player
            score = minimax(board, depth+1, True, ai_player, human_player)
            board[move] = ' '
            if score < best_score:
                best_score = score
        return best_score

def best_move(board, ai_player, human_player):
    best_score = -math.inf
    move_chosen = None
    for move in available_moves(board):
        board[move] = ai_player
        score = minimax(board, 0, False, ai_player, human_player)
        board[move] = ' '
        if score > best_score:
            best_score = score
            move_chosen = move
    return move_chosen

def human_turn(board, human_player):
    while True:
        try:
            choice = input(f"Elige casilla (1-9) para '{human_player}': ").strip()
            if choice.lower() in ('q','quit','salir'):
                print("Saliendo del juego.")
                exit()
            pos = int(choice) - 1
            if pos not in range(9):
                print("Número fuera de rango. Intenta de nuevo.")
                continue
            if board[pos] != ' ':
                print("Casilla ocupada. Elige otra.")
                continue
            return pos
        except ValueError:
            print("Entrada inválida. Escribe un número entre 1 y 9.")

def main():
    print("Tic-Tac-Toe — Humano vs Máquina (IA con minimax)")
    print("Escribe 'q' o 'quit' para salir en cualquier momento.")
    while True:
        human_player = input("¿Quieres jugar con X u O? (X empieza) [X/O]: ").strip().upper()
        if human_player in ('X','O'):
            break
        print("Respuesta inválida. Elige 'X' o 'O'.")

    ai_player = 'O' if human_player == 'X' else 'X'
    human_starts = (human_player == 'X')

    board = [' '] * 9
    current_is_human = human_starts

    print_board(board)

    while True:
        if current_is_human:
            pos = human_turn(board, human_player)
            board[pos] = human_player
        else:
            print("Máquina pensando...")
            pos = best_move(board, ai_player, human_player)
            if pos is None:
                pos = available_moves(board)[0]
            board[pos] = ai_player
            print(f"La máquina coloca '{ai_player}' en la casilla {pos+1}.")

        print_board(board)
        winner = check_winner(board)
        if winner:
            if winner == 'Tie':
                print("Empate. Buen combate.")
            else:
                if winner == human_player:
                    print("¡Felicidades! Ganaste. Eso estuvo bien.")
                else:
                    print("La máquina gana. Estuvo calculado.")
            break

        current_is_human = not current_is_human

    print("Fin del juego. Gracias por jugar.")

if __name__ == "__main__":
    main()