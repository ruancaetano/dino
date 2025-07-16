import sys
import game
import controller

def main():
    if len(sys.argv) < 2:
        print("🎮 Dino Game - Choose your mode:")
        print("1. python main.py play     - Play with keyboard")
        print("2. python main.py train    - Neural network training mode")
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
        print("🎮 Starting Neural Network Training Mode")
        print("🦖 5 Dinosaurs with Neural Network AI")
        print("🧠 Training neural networks for decision making...")
        print("=" * 40)
        run_game(5, 'train')
        
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
        game_count = 0
        
        while True:
            game_count += 1
            print(f"\n🎮 Starting Game #{game_count}")
            
            game_obj = game.Game(num_dinos, controller_type)
            game_obj.setup()
            game_obj.start()
            
            # For training mode, automatically continue without asking
            if controller_type == 'train':
                print(f"🏁 Game #{game_count} finished! Starting next game...")
                continue
            else:
                # Ask if player wants to play again (for non-training modes)
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


