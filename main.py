import sys
import game
import controller

def main():
    if len(sys.argv) < 2:
        print("🎮 Dino Game - Choose your mode:")
        print("1. python main.py play     - Play with keyboard")
        print("2. python main.py train    - Training mode")
        print("3. python main.py auto     - Auto-play with trained model")
        print("\nExample: python main.py play")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == 'play':
        print("🎮 Starting Keyboard Mode")
        print("🦖 1 Dinosaur with Keyboard Controller")
        print("=" * 40)
        run_game(1, 'keyboard')
        
    elif mode == 'train':
        print("🎮 Starting Training Mode")
        print("🦖 5 Dinosaurs with Random Controller")
        print("📊 Collecting training data...")
        print("=" * 40)
        run_game(5, 'random')
        
    elif mode == 'auto':
        print("🎮 Starting Auto Mode")
        print("🦖 3 Dinosaurs with Trained Model")
        print("🤖 Using last trained model...")
        print("=" * 40)
        run_game(3, 'trained')
        
    else:
        print(f"❌ Unknown mode: {mode}")
        print("Available modes: play, train, auto")
        sys.exit(1)

def run_game(num_dinos, controller_type):
    try:
        while True:
            game_obj = game.Game(num_dinos, controller_type)
            game_obj.setup()
            game_obj.start()
            
            # Ask if player wants to play again
            print("\n🔄 Game Over! Play again? (y/n): ", end="")
            if input().lower() != 'y':
                print("👋 Thanks for playing!")
                break
                
    except KeyboardInterrupt:
        print("\n👋 Game interrupted. Thanks for playing!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()


