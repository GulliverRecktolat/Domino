import random


def is_number(x):
    try:
        int(x)
        return True
    except:
        return False


def list_of_dominoes():
    array = []
    for first in range(7):
        for second in range(first, 7):
            array.append([first, second])
    return array


def pacs_validation(computer_pack, player_pack):
    status = None
    domino_snake = None
    for domino in computer_pack:
        if domino[0] == domino[1] and (domino_snake is None or domino[0] > domino_snake[1]):
            domino_snake = domino
            status = "player"
    for domino in player_pack:
        if domino[0] == domino[1] and (domino_snake is None or domino[0] > domino_snake[1]):
            domino_snake = domino
            status = "computer"
    if status is not None:
        return status, [domino_snake]
    else:
        return None


class Domino:
    def __init__(self):
        self.domino_snake = None
        self.STATUS = None
        self.chosen_dominoes = None
        self.stock_dominoes = None
        self.computer_pack = None
        self.player_pack = None
        self.stock_numbers_counter = [0] * 7
        while self.game_creation() == "Validation error":
            self.game_creation()
        self.stock_numbers_counter[self.domino_snake[-1][0]] += 2
        self.moves()

    def game_creation(self):
        self.chosen_dominoes = random.sample(list_of_dominoes(), k=14)
        self.stock_dominoes = [element for element in list_of_dominoes() if element not in self.chosen_dominoes]
        self.computer_pack = self.chosen_dominoes[7:]
        self.player_pack = self.chosen_dominoes[:7]
        if pacs_validation(self.computer_pack, self.player_pack) is None:
            return "Validation error"
        else:
            self.STATUS, self.domino_snake = pacs_validation(self.computer_pack, self.player_pack)
            if self.STATUS == "computer":
                # print(self.player_pack, 'player', self.domino_snake)
                self.player_pack.remove(self.domino_snake[0])
            else:
                # print(self.computer_pack, "computer", self.domino_snake)
                self.computer_pack.remove(self.domino_snake[0])

    def moves(self):
        while True:
            if len(self.player_pack) == 0 or len(self.computer_pack) == 0:
                break
            #print(self.stock_numbers_counter)
            for number in range(len(self.stock_numbers_counter)):
                if self.stock_numbers_counter[number] == 8 and \
                        self.domino_snake[0][0] == number and self.domino_snake[-1][-1] == number:
                    break
            print('=' * 70)
            print('Stock size:', len(self.stock_dominoes))
            print('Computer pieces:', len(self.computer_pack))
            if len(self.domino_snake) > 6:
                print("\n", *self.domino_snake[:3], "...", *self.domino_snake[-3:], "\n", sep="")
            else:
                print("\n", *self.domino_snake, "\n", sep="")
            print("Your pieces:")
            if len(self.player_pack) > 0:
                for i in range(len(self.player_pack)):
                    print(i + 1, ":", self.player_pack[i], sep="")
            if self.STATUS == "player":
                print("\n", "Status: It's your turn to make a move. Enter your command.", sep="")
                self.STATUS = "computer"
                chosen_domino = input()
                while True:
                    if not is_number(chosen_domino) or abs(int(chosen_domino)) > len(self.player_pack):
                        print("Invalid input. Please try again.")
                    elif int(chosen_domino) > 0 and \
                            self.domino_snake[-1][-1] not in self.player_pack[int(chosen_domino) - 1]:
                        print("Illegal move. Please try again.")
                    elif int(chosen_domino) < 0 and \
                            self.domino_snake[0][0] not in self.player_pack[abs(int(chosen_domino)) - 1]:
                        print("Illegal move. Please try again.")
                    elif int(chosen_domino) == 0 and len(self.stock_dominoes) == 0:
                        print("Invalid input. Please try again.")
                    else:
                        break
                    chosen_domino = input()
                chosen_domino = int(chosen_domino)
                if chosen_domino == 0:
                    self.player_pack.append(self.stock_dominoes[-1])
                    self.stock_dominoes.pop(-1)
                elif chosen_domino > 0:
                    if self.player_pack[chosen_domino - 1][0] == self.domino_snake[-1][-1]:
                        self.domino_snake.append(self.player_pack[chosen_domino - 1])
                    else:
                        self.domino_snake.append(self.player_pack[chosen_domino - 1][::-1])
                    self.player_pack.pop(chosen_domino - 1)
                    self.stock_numbers_counter[self.domino_snake[-1][0]] += 1
                    self.stock_numbers_counter[self.domino_snake[-1][-1]] += 1
                else:
                    if self.player_pack[abs(chosen_domino) - 1][1] == self.domino_snake[0][0]:
                        self.domino_snake.insert(0, self.player_pack[abs(chosen_domino) - 1])
                    else:
                        self.domino_snake.insert(0, self.player_pack[abs(chosen_domino) - 1][::-1])
                    self.player_pack.pop(abs(chosen_domino) - 1)
                    self.stock_numbers_counter[self.domino_snake[0][0]] += 1
                    self.stock_numbers_counter[self.domino_snake[0][-1]] += 1
            else:
                print("\n", "Status: Computer is about to make a move. Press Enter to continue...", sep="")
                _ = input()
                #print(self.computer_pack)
                current_numbers_counter = [i for i in self.stock_numbers_counter]
                for domino in self.computer_pack:
                    current_numbers_counter[domino[0]] += 1
                    current_numbers_counter[domino[1]] += 1
                current_moves = {}
                for i in range(len(self.computer_pack)):
                    if self.domino_snake[-1][-1] in self.computer_pack[i]:
                        if self.computer_pack[i][0] == self.domino_snake[-1][-1]:
                            score = current_numbers_counter[self.computer_pack[i][0]] +\
                                    current_numbers_counter[self.computer_pack[i][1]]
                            current_moves[score] = [self.computer_pack[i], "finish"]
                        else:
                            score = current_numbers_counter[self.computer_pack[i][0]] + \
                                    current_numbers_counter[self.computer_pack[i][1]]
                            current_moves[score] = [self.computer_pack[i][::-1], "finish"]
                    elif self.domino_snake[0][0] in self.computer_pack[i]:
                        if self.computer_pack[i][1] == self.domino_snake[0][0]:
                            score = current_numbers_counter[self.computer_pack[i][0]] + \
                                    current_numbers_counter[self.computer_pack[i][1]]
                            current_moves[score] = [self.computer_pack[i], "start"]
                        else:
                            score = current_numbers_counter[self.computer_pack[i][0]] + \
                                    current_numbers_counter[self.computer_pack[i][1]]
                            current_moves[score] = [self.computer_pack[i][::-1], "start"]
                if len(current_moves) > 0:
                    current_moves = list(current_moves.items())
                    current_moves.sort(key=lambda x: x[0], reverse=True)
                    #print(current_moves)
                    if current_moves[0][1][1] == "start":
                        self.domino_snake.insert(0, current_moves[0][1][0])
                        self.stock_numbers_counter[current_moves[0][1][0][0]] += 1
                        self.stock_numbers_counter[current_moves[0][1][0][1]] += 1
                        if current_moves[0][1][0] in self.computer_pack:
                            self.computer_pack.remove(current_moves[0][1][0])
                        else:
                            self.computer_pack.remove(current_moves[0][1][0][::-1])
                    else:
                        self.domino_snake.append(current_moves[0][1][0])
                        self.stock_numbers_counter[current_moves[0][1][0][0]] += 1
                        self.stock_numbers_counter[current_moves[0][1][0][1]] += 1
                        if current_moves[0][1][0] in self.computer_pack:
                            self.computer_pack.remove(current_moves[0][1][0])
                        else:
                            self.computer_pack.remove(current_moves[0][1][0][::-1])
                elif len(current_moves) == 0:
                    if len(self.stock_dominoes) > 0:
                        self.computer_pack.append(random.choice(self.stock_dominoes))
                        self.stock_dominoes.remove(self.computer_pack[-1])
                    else:
                        break
                self.STATUS = "player"

        print('=' * 70)
        print('Stock size:', len(self.stock_dominoes))
        print('Computer pieces:', len(self.computer_pack))
        if len(self.domino_snake) > 6:
            print("\n", *self.domino_snake[:3], "...", *self.domino_snake[-3:], "\n", sep="")
        else:
            print("\n", *self.domino_snake, "\n", sep="")
        print("Your pieces:")
        if len(self.player_pack) > 0:
            for i in range(len(self.player_pack)):
                print(i + 1, ":", self.player_pack[i], sep="")
        if len(self.player_pack) == 0:
            print("\n", "Status: The game is over. You won!", sep="")
        elif len(self.computer_pack) == 0:
            print("\n", "Status: The game is over. The computer won!", sep="")
        else:
            print("\n", "Status: The game is over. It's a draw!", sep="")


if __name__ == "__main__":
    Domino()
