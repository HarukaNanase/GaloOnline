def CurrentBoard(Board):
    print("\n", Board.get("0"),"|",Board.get("1"),"|",Board.get("2"),
          "\n---+---+---\n",Board.get("3"),"|",Board.get("4"),"|",Board.get("5"),
          "\n---+---+---\n",Board.get("6"),"|",Board.get("7"),"|",Board.get("8"))


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
    play = input("Introduza a sua jogada (0-8): ")

    if int(play) not in (0, 1, 2, 3, 4, 5, 6, 7, 8):
        print("Jogada Invalida (Não introduziu um numero de 0 a 8).")
        return False
    if Board.get(play) not in (0, 1, 2, 3, 4, 5, 6, 7, 8):
        print("Espaço ocupado.")
        return False
    else:
        return play


def Play(Board,Position, Symbol):
    Board[Position] = Symbol
