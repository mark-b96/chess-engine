from game_controller import GameController
import time


def game():
    game_controller = GameController()
    while 1:
        if game_controller.board.checkmate or game_controller.board.stalemate:
            break
        game_controller.human_move()
        if game_controller.board.checkmate or game_controller.board.stalemate:
            break
        game_controller.ai_move()
    while 1:
        pass


def main():
    game()


if __name__ == '__main__':
    main()
