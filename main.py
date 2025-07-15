import game

if __name__ == '__main__':
    while True:
        game_obj = game.Game(10)
        game_obj.setup()
        game_obj.start()

