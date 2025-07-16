import sys
from game.game import Game

def main():
    if len(sys.argv) < 2:
        print("Dino Game - Choose your mode:")
        print("1. python main.py play     - Play with keyboard")
        print("2. python main.py train    - Genetic algorithm training mode")
        print("3. python main.py auto     - Auto-play with trained model")
        print("\nExample: python main.py play")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == 'play':
        print("Starting Keyboard Mode")
        print("1 Dinosaur with Keyboard Controller")
        print("=" * 40)
        run_game(1, 'keyboard')
        
    elif mode == 'train':
        print("Starting Genetic Algorithm Training Mode")
        print("50 Dinosaurs with Genetic Algorithm")
        print("Evolving neural networks through natural selection...")
        print("=" * 40)
        # Use the dedicated training module
        from train.train import main as train_main
        train_main()
        
    elif mode == 'auto':
        print("Starting Auto Mode")
        print("3 Dinosaurs with Neural Network AI")
        print("Using neural network for decision making...")
        print("=" * 40)
        run_game(1, 'auto')
        
    else:
        print(f"Unknown mode: {mode}")
        print("Available modes: play, train, auto")
        sys.exit(1)

def run_game(num_dinos, controller_type):
    try:
        print("Game started!")
        
        game_obj = Game(num_dinos, controller_type)
        game_obj.setup()
        game_obj.start()
                
    except KeyboardInterrupt:
        print("\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()


