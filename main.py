import random

class Player:
    def __init__(self, name, agent, credits):
        self.name = name
        self.agent = agent
        self.credits = credits
        self.health = 100
        self.armor = 0
        self.position = (0, 0)  # (x, y) coordinates
        self.weapon = "Pistol"  # Default weapon

    def take_damage(self, damage):
        total_damage = damage - self.armor
        if total_damage > 0:
            self.health -= total_damage

    def move(self, x, y):
        self.position = (self.position[0] + x, self.position[1] + y)

    def shoot(self, target):
        if self.weapon == "Pistol":
            damage = random.randint(10, 20)
        elif self.weapon == "Rifle":
            damage = random.randint(20, 30)
        elif self.weapon == "Shotgun":
            damage = random.randint(5, 15)
        else:
            damage = 0

        target.take_damage(damage)
        print(f"{self.name} shot {target.name} for {damage} damage.")

    def purchase_weapon(self):
        print("Available weapons:")
        weapons = ["Pistol", "Rifle", "Shotgun"]
        for idx, weapon in enumerate(weapons, start=1):
            print(f"{idx}. {weapon}")
        choice = int(input("Enter the weapon number you want to purchase: "))

        if choice < 1 or choice > len(weapons):
            print("Invalid choice!")
        else:
            weapon = weapons[choice - 1]
            weapon_cost = 100 if weapon == "Rifle" else 50  # Adjust the costs as needed

            if self.credits >= weapon_cost:
                self.weapon = weapon
                self.credits -= weapon_cost
                print(f"You purchased a {weapon}.")
            else:
                print("Not enough credits to purchase the weapon.")

    def shoot_attack(self, target):
        self.shoot(target)

    def move_attack(self, target):
        move_direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.move(*move_direction)
        print(f"{self.name} moved to {self.position}.")

    def purchase_weapon_attack(self, target):
        self.purchase_weapon()

    def opponent_attack(self, target):
        attack_choice = random.choice([self.move_attack, self.shoot_attack, self.purchase_weapon_attack])
        attack_choice(target)

class Game:
    def __init__(self, mode):
        self.mode = mode
        self.agents = self.load_data("agents.txt")
        self.weapons = self.load_data("weapons.txt")

    def load_data(self, filename):
        with open(filename, "r") as file:
            return file.read().splitlines()

    def start(self):
        player1_name = input("Enter your name: ")
        agent = self.choose_agent()
        credits = 200 if self.mode == "unrated" else 0
        player1 = Player(player1_name, agent, credits)

        # Generate a random player for the opponent
        opponent_agent = random.choice(self.agents)
        opponent_credits = 200
        player2 = Player("Opponent", opponent_agent, opponent_credits)

        # Game loop
        while player1.health > 0 and player2.health > 0:
            print(f"\n=== Turn: {player1.name} ===")
            self.display_stats(player1, player2)
            self.take_turn(player1, player2)

            if not player2.health > 0:
                break

            player2.opponent_attack(player1)

        # Game Over
        if player1.health > 0:
            print(f"\nCongratulations! {player1.name} wins!")
        else:
            print("\nYou lost! Better luck next time.")

    def choose_agent(self):
        print("Choose an agent:")
        for idx, agent in enumerate(self.agents, start=1):
            print(f"{idx}. {agent}")
        choice = int(input("Enter the agent number: "))
        return self.agents[choice - 1]

    def take_turn(self, current_player, other_player):
        print("\nChoose an action:")
        print("1. Move")
        print("2. Shoot")
        print("3. Purchase Weapon")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            current_player.move_attack(other_player)
        elif choice == 2:
            current_player.shoot_attack(other_player)
        elif choice == 3:
            current_player.purchase_weapon_attack(other_player)
        else:
            print("Invalid choice!")

    def display_stats(self, player, opponent):
        print(f"\n{player.name}'s Stats:")
        print(f"Agent: {player.agent}")
        print(f"Weapon: {player.weapon}")
        print(f"Credits: {player.credits}")
        print(f"Health: {player.health}")
        print(f"Armor: {player.armor}")

        print(f"\n{opponent.name}'s Stats:")
        print(f"Agent: {opponent.agent}")
        print(f"Weapon: {opponent.weapon}")
        print(f"Health: {opponent.health}")
        print(f"Armor: {opponent.armor}")

def main():
    print("Welcome to Text-Based Valorant!")
    print("Choose a mode:")
    print("1. Unrated")
    print("2. Competitive")
    print("3. Team Death Match")
    mode_choice = int(input("Enter the mode number: "))

    if mode_choice == 1:
        mode = "unrated"
    elif mode_choice == 2:
        mode = "competitive"
    elif mode_choice == 3:
        mode = "team_death_match"
    else:
        print("Invalid choice!")
        return

    game = Game(mode)
    game.start()

if __name__ == "__main__":
    main()
