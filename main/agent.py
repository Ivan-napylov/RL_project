import random
from hexmap import HexMap
from army import Soldier
import numpy as np

class Agent:
    def __init__(self, name, hex_map, color, initial_cells, coin_system):
        self.name = name
        self.hex_map = hex_map
        # self.hex_map.grid[self.position].owner = name
        # self.hex_map.grid[self.position].owner_color = color
        self.hex_map.generate_user_land(initial_cells, name, color)
        self.score = 0
        self.color = color
        self.coin_system = coin_system
        self.soldiers = []

    def choose_action(self, action_type=None, random_=False):
        # Decide action type: 0 = Move soldier, 1 = Add Soldier, 2 = Expand Territory
        owned_territory = self.get_owned_territory()
        soldier_positions = self.get_soldier_positions()
        
        if random_:
            action_type = random.choice([0, 1])
        
        # Add Soldier: Ensure there are enough coins to add a soldier
        if action_type == 1 and self.coin_system.balance >= 10:  # Assuming 'coins' is the available coins
            # Randomly select a cell within owned territory or adjacent to it
            target_cell = random.choice(owned_territory + self.get_adjacent_land(owned_territory))
            if target_cell:
                q, r = target_cell
                # soldier_level = random.choice([1, 2, 3])  # Random soldier level, you can adjust logic
                if self.add_soldier(q, r, soldier_level=1):
                    return  # Successfully added soldier
        
        # Move Soldier: Only move a soldier if there are soldiers to move and valid destination
        elif action_type == 0 and soldier_positions:
            # Pick a random soldier and move it to a valid neighboring position
            from_q, from_r = random.choice(soldier_positions)
            neighbors = self.hex_map.get_neighbors(from_q, from_r)
            for to_q, to_r in neighbors:
                if self.hex_map.is_user_land(to_q, to_r, self.name) or self.hex_map.grid[(to_q, to_r)].owner is None:
                    if self.move_soldier(from_q, from_r, to_q, to_r):
                        return  # Successfully moved soldier and expanded territory
        
        return None  # No valid action could be performed
    
    
    def add_soldier(self, q, r, soldier_level=1):
        soldier = Soldier(level=soldier_level)
        # Place a soldier in the given cell if it's empty
        if self.hex_map.is_user_land(q, r, self.name) or self.hex_map.is_adjacent_to_user_land(q, r, self.name):
            if self.coin_system.spend(soldier.cost) and self.hex_map.grid.get((q, r)) and not self.hex_map.grid[(q, r)].content:
                enemy = self.hex_map.grid[(q, r)].owner
                print("Enemy", enemy)
                if  enemy and enemy != self.name:
                    self.coin_system.balance += 5
                self.hex_map.grid[(q, r)].content = soldier
                self.hex_map.grid[(q, r)].owner = self.name
                self.hex_map.grid[(q, r)].owner_color = self.color
                self.soldiers.append((q, r))  # Track the soldier's position
                return True
            else:
                return False
    
    def move_soldier(self, from_q, from_r, to_q, to_r):
        """Move a soldier from one hex to another if valid."""
        from_cell = self.hex_map.grid.get((from_q, from_r))
        to_cell = self.hex_map.grid.get((to_q, to_r))

        if not from_cell or not to_cell:
            return False

        # Ensure the 'from' cell has a soldier and belongs to the user
        if from_cell.owner != self.name or not isinstance(from_cell.content, Soldier):
            return False
        
        if isinstance(to_cell.content, Soldier):
            return False
        
        # if to_cell.owner != self.name and to_cell.owner is not None:
        #     to_cell.owner = self.name
        #     to_cell.owner_color = self.color

        if (
            (from_q, from_r) in self.soldiers and (to_q, to_r) in self.hex_map.get_neighbors(from_q, from_r)
        ):
            if not to_cell.owner:
                self.coin_system.balance += 5
            elif to_cell.owner and to_cell.owner != self.name:
                print("Remove opponent")
                self.coin_system.balance += 10

            soldier = self.hex_map.grid[(from_q, from_r)].content
            self.hex_map.grid[(from_q, from_r)].content = None
            self.hex_map.grid[(to_q, to_r)].content = soldier
            self.hex_map.grid[(to_q, to_r)].owner_color = self.color
            self.hex_map.grid[(to_q, to_r)].owner = self.name
            self.soldiers.remove((from_q, from_r))
            self.soldiers.append((to_q, to_r))

            # print(f"{self.name} moved a soldier from ({from_q}, {from_r}) to ({to_q}, {to_r}).")
            return True
        else:
            # print(f"{self.name} failed to move a soldier from ({from_q}, {from_r}) to ({to_q}, {to_r}).")
            return False
    
    def get_owned_territory(self):
        """Return a list of hex coordinates owned by the agent."""
        return [coords for coords, cell in self.hex_map.grid.items() if cell.owner == self.name]

    def get_soldier_positions(self):
        """Return the positions of all soldiers owned by the agent."""
        return self.soldiers

    def get_adjacent_land(self, owned_territory):
        """Return a list of coordinates for cells adjacent to the agent's owned territory."""
        adjacent_land = []
        for (q, r) in owned_territory:
            # Get the neighbors of the current hex (q, r)
            neighbors = self.hex_map.get_neighbors(q, r)  # assuming 'get_neighbors' returns adjacent hexes
            for neighbor in neighbors:
                nq, nr = neighbor
                # Check if the neighbor is valid (within the map bounds)
                if self.hex_map.is_valid_location(nq, nr):
                    # Check if the neighboring cell is unclaimed (can be expanded into)
                    cell = self.hex_map.grid.get((nq, nr))
                    if cell and cell.owner is None:
                        adjacent_land.append((nq, nr))  # Add the neighbor if it's unclaimed
        return adjacent_land
    
    def calculate_reward(self, action):
        self.action_space = ["collect_coin", "spend_coin", "expand_territory"]
        action_str = self.action_space[action]
        # Basic reward structure: Coins earned or spent during actions
        if action_str == "collect_coin":
            # Reward for collecting coins
            reward = 10  # Reward for each coin collected, can be adjusted based on game mechanics
        elif action_str == "spend_coin":
            # Penalize for spending coins if it's not a strategic action
            reward = -5  # Deduct coins as a penalty for spending (can be adjusted)
        elif action_str == "expand_territory":
            # Reward for expanding territory (which may generate coins over time)
            reward = 20  # Reward for expanding territory
        else:
            # Neutral reward for other actions or invalid actions
            reward = 0

        # Bonus or penalty for the agent's coin balance
        coin_balance = self.coin_system.balance  # Get the current coin balance of the agent
        if coin_balance > 100:
            reward += 5  # Reward if the agent has more than 100 coins
        elif coin_balance < 20:
            reward -= 5  # Penalize if the agent has fewer than 20 coins
        
        return reward
    
    def get_state(self, enemy):
        # Get all grid keys (coordinates) for the hex map, for later use in grid representation
        grid_keys = list(self.hex_map.grid.keys())
        
        # Initialize an empty list to hold each part of the state
        state = []

        # 1. Coin balance of the agent (ensure it's a 1D numpy array)
        state.append(np.array([self.coin_system.balance]))

        # 2. Flatten the agent's owned territory (binary representation)
        agent_territory_map = np.zeros(len(grid_keys))  # Initialize as zero for all cells
        owned_territory = self.get_owned_territory()
        for idx, (q, r) in enumerate(grid_keys):
            if (q, r) in owned_territory:
                agent_territory_map[idx] = 1
        state.append(agent_territory_map.flatten())  # Flatten to 1D array

        # 3. Flatten the enemy's owned territory (binary representation)
        enemy_territory_map = np.zeros(len(grid_keys))  # Initialize as zero for all cells
        enemy_territory = enemy.get_owned_territory()
        
        for idx, (q, r) in enumerate(grid_keys):
            if (q, r) in enemy_territory:
                enemy_territory_map[idx] = 1
        state.append(enemy_territory_map.flatten())  # Flatten to 1D array

        # 4. Flatten the grid representation (ownership and troops, etc.)
        grid_rep = np.zeros(len(grid_keys))  # Initialize with zero for all cells
        for idx, (q, r) in enumerate(grid_keys):
            cell = self.hex_map.grid[(q, r)]
            if cell.owner == self.name:
                grid_rep[idx] = 1  # Owned by the agent
            elif cell.owner == enemy.name:
                grid_rep[idx] = 2  # Owned by the enemy
        state.append(grid_rep.flatten())  # Flatten to 1D array
        # Convert the state list to a numpy array for easier manipulation
        state = np.concatenate(state)  # Concatenate all the 1D arrays

        return state


