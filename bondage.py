import random
import time
import json
import os

def print_slow(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.015)
    print()

class BodangeGame:
    def __init__(self):
        self.hours_survived = 0
        self.belgian_morale = 100
        self.ammo = 50
        self.german_strength = 10
        self.save_file = "bodange_save.json"

    def save_game(self):
        """Saves the current game state to a JSON file."""
        game_data = {
            "hours_survived": self.hours_survived,
            "belgian_morale": self.belgian_morale,
            "ammo": self.ammo,
            "german_strength": self.german_strength
        }
        with open(self.save_file, 'w') as f:
            json.dump(game_data, f)
        print_slow(f"\n[ Game progress saved to {self.save_file} ]")

    def load_game(self):
        """Loads a game state from a JSON file if it exists."""
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as f:
                game_data = json.load(f)
                self.hours_survived = game_data["hours_survived"]
                self.belgian_morale = game_data["belgian_morale"]
                self.ammo = game_data["ammo"]
                self.german_strength = game_data["german_strength"]
            print_slow("\n[ Previous save file loaded successfully! ]")
            return True
        return False

    def player_turn(self):
        print(f"\n--- HOUR {self.hours_survived + 1} ---")
        print(f"Morale: {self.belgian_morale}% | Ammo: {self.ammo} crates | Enemy Strength: {self.german_strength}")
        
        print("\nOrders:")
        print("1. Hold the line (Cost: 10 Ammo, Drops Enemy Strength)")
        print("2. Fall back (Boosts Morale, Enemy Advances)")
        print("3. Demolish road (Cost: 5 Ammo, Delays Enemy)")
        print("4. Save Game")
        
        choice = input("Enter 1, 2, 3, or 4: ")

        if choice == '1':
            if self.ammo >= 10:
                print_slow("> Chasseurs lay down heavy fire!")
                self.ammo -= 10
                self.german_strength -= random.randint(2, 4)
            else:
                print_slow("> Out of ammo! The Germans advance freely.")
                self.german_strength += 3
        elif choice == '2':
            print_slow("> Troops fall back to defensive cover.")
            self.belgian_morale += 15
            self.german_strength += random.randint(2, 5)
        elif choice == '3':
            if self.ammo >= 5:
                print_slow("> Obstacles destroyed! The enemy is delayed.")
                self.ammo -= 5
                self.german_strength -= 1
            else:
                print_slow("> No explosives left!")
                self.german_strength += 2
        elif choice == '4':
            self.save_game()
            return False # Skip enemy phase if just saving
        else:
            print_slow("> Invalid command. Chaos in the ranks!")
            self.belgian_morale -= 5
            
        return True # Proceed to enemy phase

    def enemy_turn(self):
        print_slow("\n[ Enemy Phase ]")
        # Ensure enemy strength doesn't drop below 1 for math reasons
        self.german_strength = max(1, self.german_strength) 
        
        damage = self.german_strength * random.randint(1, 3)
        print_slow(f"> The 1st Panzer Division fires barrage! (-{damage} Morale)")
        self.belgian_morale -= damage
        
        self.german_strength += 2 
        self.hours_survived += 1
        time.sleep(1)

    def run(self):
        print_slow("========================================")
        print_slow("      THE BATTLE OF BODANGE (1940)      ")
        print_slow("========================================")
        
        load_prompt = input("Do you want to load a saved game? (y/n): ").lower()
        if load_prompt == 'y':
            if not self.load_game():
                print_slow("> No save file found. Starting a new campaign.")
                
        while self.hours_survived < 10 and self.belgian_morale > 0:
            turn_completed = self.player_turn()
            if turn_completed:
                self.enemy_turn()

        print("\n========================================")
        if self.belgian_morale > 0:
            print_slow("VICTORY! You held the line against overwhelming odds.")
        else:
            print_slow("DEFEAT. Your lines were overrun.")
        print("========================================")

if __name__ == "__main__":
    game = BodangeGame()
    game.run()
