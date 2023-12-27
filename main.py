import game

if __name__ == '__main__':
    while True:
        game_obj = game.Game(50)
        game_obj.setup()
        game_obj.start()

