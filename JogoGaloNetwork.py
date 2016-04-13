def NewBoard():
    i = 0
    Board = {}
    while i < 9:
        Board[str(i)] = i
        i += 1
    return Board


def CheckWinner(Board):
    if Board.get(str(0)) == Board.get(str(1)) == Board.get(str(2)):
        return True
    elif Board.get(str(3)) == Board.get(str(4)) == Board.get(str(5)):
        return True
    elif Board.get(str(6)) == Board.get(str(7)) == Board.get(str(8)):
        return True
    elif Board.get(str(0)) == Board.get(str(3)) == Board.get(str(6)):
        return True
    elif Board.get(str(1)) == Board.get(str(4)) == Board.get(str(7)):
        return True
    elif Board.get(str(2)) == Board.get(str(5)) == Board.get(str(8)):
        return True
    elif Board.get(str(0)) == Board.get(str(4)) == Board.get(str(8)):
        return True
    elif Board.get(str(6)) == Board.get(str(4)) == Board.get(str(2)):
        return True
    else:
        return False


def ReadPlay(Board):
    play = input("Introduza a sua jogada (1-9): ")
    if int(play) not in (1, 2, 3, 4, 5, 6, 7, 8):
        print("Jogada Invalida (Não introduziu um numero de 1 a 9).")
        return False
    if Board.get(play) not in (1, 2, 3, 4, 5, 6, 7, 8):
        print("Espaço ocupado.")
        return False
    else:
        return play


def Play(Board,Position, Symbol):
    Board[Position] = Symbol
