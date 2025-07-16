import pygame
import time
from game import game, state, floor, dino, event, colors, configs, cloud
from controllers import genetic_controller

class GeneticTrainer(game.Game):
    def __init__(self, population_size: int = 50):
        # Initialize with population size instead of dinos_quantities
        super().__init__(population_size, 'genetic')
        
        self.population_size = population_size
        self.genetic_manager = genetic_controller.GeneticGameManager(population_size=population_size)
        
        # Training state
        self.generation = 0
        self.best_fitness = 0
        
    def setup(self):
        """Override setup to use genetic controllers instead of regular controllers"""
        # Create fresh game state
        self.game_state = state.GameState()
        self.game_state.start_game()
        
        # Clear all sprite groups
        self.game_state.all_sprites_group.empty()
        self.game_state.trees_sprites_group.empty()
        self.dino_sprites.clear()
        
        # Clear dino data
        self.game_state.points.clear()
        self.game_state.dino_rects_map.clear()
        
        # Create floor
        self.floor_sprite = floor.Floor()
        self.game_state.all_sprites_group.add(self.floor_sprite)
        self.game_state.floor_rect = self.floor_sprite.rect
        
        # Create dinos with genetic controllers
        genetic_controllers = self.genetic_manager.get_controllers_for_game(self.population_size, self.game_state)
        
        for index in range(self.population_size):
            dino_id = index + 1
            dino_controller = genetic_controllers[index]
            
            dino_sprite = dino.Dino(dino_id, self.game_state, dino_controller)
            self.dino_sprites.append(dino_sprite)
            self.game_state.all_sprites_group.add(dino_sprite)
            self.game_state.dino_rects_map[dino_id] = dino_sprite.rect
            self.game_state.points[dino_id] = 0
        
        # Create event manager
        self.event_manager = event.EventManager(self.game_state)
        
    def run_game_loop(self):
        """Run the game loop for one generation"""
        while self.game_state.running and len(self.dino_sprites) > 0:
            self.screen.fill(colors.BLUE_RGB)
            
            # Handle events
            if self.event_manager:
                self.event_manager.produce_events()
                self.event_manager.handle_events()
            
            # Update and draw sprites
            self.update_sprites()
            
            # Check collisions
            self.verify_collisions()
            
            # Draw HUD
            self.draw_hud()
            
            pygame.display.update()
            self.clock.tick(configs.CLOCK_TICK)
    
    def draw_hud(self):
        """Override draw_hud to show training-specific information"""
        # Draw score
        score_text = self.font.render(f"Score: {self.game_state.max_point}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        # Draw speed and level
        speed_level = max(0, (self.game_state.max_point - 1) // 20)
        current_speed = configs.BASE_GAME_SPEED + (speed_level * configs.SPEED_INCREASE_RATE)
        speed_text = self.font.render(f"Speed: {current_speed:.1f} (Level: {speed_level})", True, (255, 255, 255))
        self.screen.blit(speed_text, (10, 50))
        
        # Draw generation info
        gen_text = self.font.render(f"Generation: {self.generation}", True, (255, 255, 255))
        self.screen.blit(gen_text, (10, 90))
        
        # Draw dinos alive
        dinos_text = self.font.render(f"Dinos Alive: {len(self.dino_sprites)}", True, (255, 255, 255))
        self.screen.blit(dinos_text, (10, 130))
        
        # Draw FPS
        fps = self.clock.get_fps()
        fps_text = self.fps_font.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 170))
        
        # Draw top scores
        self.draw_top_scores()
    
    def evolve_population(self):
        """Evolve the population based on current game results"""
        # Ensure all dinos have scores
        game_results = []
        for dino_id in range(1, self.population_size + 1):
            score = self.game_state.points.get(dino_id, 0)
            game_results.append((dino_id, score))
        
        # Evolve the population
        self.genetic_manager.evolve_population(game_results)
        self.generation += 1
        
        # Save best individual periodically
        if self.generation % 5 == 0:
            self.genetic_manager.ga.save_best_individual()
    
    def train(self, max_generations: int = 1000):
        """Main training loop"""
        print(f"Starting genetic training with {self.population_size} dinos")
        print("Press Ctrl+C to stop training")
        
        try:
            while self.generation < max_generations:
                # Setup new game
                self.setup()
                
                # Run the game until all dinos die
                self.run_game_loop()
                
                # Evolve population
                self.evolve_population()
                
        except KeyboardInterrupt:
            print("\nTraining stopped by user")
            self.genetic_manager.ga.save_best_individual()
        
        pygame.quit()

def main():
    """Entry point for training mode"""
    trainer = GeneticTrainer(population_size=50)
    trainer.setup()
    trainer.train(max_generations=1000)

if __name__ == '__main__':
    main()