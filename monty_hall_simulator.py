import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

class MontyHallSimulator:
    def __init__(self):
        """Initialize the Monty Hall simulator"""
        self.results_switch = []
        self.results_stay = []
        self.cumulative_win_rate_switch = []
        self.cumulative_win_rate_stay = []
        
    def run_single_game(self, switch=True):
        """
        Simulate a single game of the Monty Hall problem
        
        Args:
            switch (bool): Whether the player switches doors after the host reveals one
            
        Returns:
            bool: Whether the player won the car
        """
        # Place the car behind one of the three doors randomly
        car_door = np.random.randint(0, 3)
        
        # Player chooses a door randomly
        player_choice = np.random.randint(0, 3)
        
        # Host reveals a goat door (not the car, not the player's choice)
        possible_doors = [i for i in range(3) if i != car_door and i != player_choice]
        # If player picked the car, host can choose any of the other doors with goats
        if possible_doors:
            host_reveal = np.random.choice(possible_doors)
        else:
            # If player picked a goat, host must reveal the other goat
            host_reveal = [i for i in range(3) if i != car_door and i != player_choice][0]
        
        # Player decides whether to switch doors
        if switch:
            # Player switches to the door that is neither their original choice nor the revealed door
            final_choice = [i for i in range(3) if i != player_choice and i != host_reveal][0]
        else:
            # Player sticks with original choice
            final_choice = player_choice
        
        # Win if final choice is the car door
        return final_choice == car_door
    
    def run_simulation(self, num_trials=10000):
        """
        Run multiple trials of the Monty Hall problem
        
        Args:
            num_trials (int): Number of games to simulate
        """
        self.results_switch = []
        self.results_stay = []
        self.cumulative_win_rate_switch = []
        self.cumulative_win_rate_stay = []
        
        for i in range(num_trials):
            # Simulate a game where the player switches
            result_switch = self.run_single_game(switch=True)
            self.results_switch.append(result_switch)
            
            # Simulate a game where the player stays
            result_stay = self.run_single_game(switch=False)
            self.results_stay.append(result_stay)
            
            # Calculate cumulative win rates
            self.cumulative_win_rate_switch.append(sum(self.results_switch) / len(self.results_switch))
            self.cumulative_win_rate_stay.append(sum(self.results_stay) / len(self.results_stay))
    
    def plot_results(self):
        """Plot the results of the simulation"""
        # Set style
        sns.set(style="whitegrid")
        
        # Create a figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot the win rates as a bar chart
        strategy_names = ['Switch', 'Stay']
        win_rates = [
            sum(self.results_switch) / len(self.results_switch),
            sum(self.results_stay) / len(self.results_stay)
        ]
        
        bars = ax1.bar(strategy_names, win_rates, color=['#3498db', '#e74c3c'])
        ax1.set_ylim(0, 1)
        ax1.set_ylabel('Win Rate')
        ax1.set_title('Win Rates by Strategy')
        
        # Add text labels on the bars
        for bar, rate in zip(bars, win_rates):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{rate:.2%}', ha='center', va='bottom', fontweight='bold')
        
        # Plot the convergence of win rates over trials
        trials = range(1, len(self.cumulative_win_rate_switch) + 1)
        ax2.plot(trials, self.cumulative_win_rate_switch, label='Switch', color='#3498db')
        ax2.plot(trials, self.cumulative_win_rate_stay, label='Stay', color='#e74c3c')
        ax2.axhline(y=2/3, linestyle='--', color='#3498db', alpha=0.5, label='Expected (Switch): 2/3')
        ax2.axhline(y=1/3, linestyle='--', color='#e74c3c', alpha=0.5, label='Expected (Stay): 1/3')
        
        ax2.set_xlabel('Number of Trials')
        ax2.set_ylabel('Cumulative Win Rate')
        ax2.set_title('Convergence of Win Rates')
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig('monty_hall_results.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_animated_simulation(self, num_frames=100):
        """
        Create an animation showing how win rates converge over time
        
        Args:
            num_frames (int): Number of frames in the animation
            
        Returns:
            HTML: HTML object containing the animation
        """
        # Run a simulation with more trials to get data for animation
        self.run_simulation(num_trials=num_frames*100)
        
        # Set up the figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Initialize lines
        switch_line, = ax.plot([], [], 'b-', lw=2, label='Switch')
        stay_line, = ax.plot([], [], 'r-', lw=2, label='Stay')
        expected_switch = ax.axhline(y=2/3, linestyle='--', color='blue', alpha=0.5, label='Expected (Switch): 2/3')
        expected_stay = ax.axhline(y=1/3, linestyle='--', color='red', alpha=0.5, label='Expected (Stay): 1/3')
        
        # Set up plot
        ax.set_xlim(0, num_frames*100)
        ax.set_ylim(0, 1)
        ax.set_xlabel('Number of Trials')
        ax.set_ylabel('Win Rate')
        ax.set_title('Monty Hall Problem - Win Rate Convergence')
        ax.legend(loc='center right')
        ax.grid(True)
        
        # Animation function
        def animate(i):
            x = range(1, i*100 + 1)
            switch_line.set_data(x, self.cumulative_win_rate_switch[:i*100])
            stay_line.set_data(x, self.cumulative_win_rate_stay[:i*100])
            return switch_line, stay_line
        
        # Create animation
        anim = FuncAnimation(fig, animate, frames=num_frames, interval=50, blit=True)
        plt.close()  # Prevent display of static plot
        
        # Save animation
        anim.save('monty_hall_animation.gif', writer='pillow', fps=10, dpi=80)
        
        return anim
    
    def visualize_game_state(self):
        """Create a visual explanation of a single game"""
        car_door = np.random.randint(0, 3)
        player_choice = np.random.randint(0, 3)
        
        # Host reveals a goat door
        possible_doors = [i for i in range(3) if i != car_door and i != player_choice]
        if possible_doors:
            host_reveal = np.random.choice(possible_doors)
        else:
            host_reveal = [i for i in range(3) if i != car_door and i != player_choice][0]
        
        # Create a 2x3 grid of subplots to show different stages
        fig, axes = plt.subplots(2, 3, figsize=(15, 8))
        
        # Door labels
        door_labels = ['Door 1', 'Door 2', 'Door 3']
        door_colors = ['#f39c12', '#f39c12', '#f39c12']  # Initial color
        
        # Stage 1: Initial setup
        axes[0, 0].bar(door_labels, [1, 1, 1], color=door_colors)
        axes[0, 0].set_title('Stage 1: Three Closed Doors')
        axes[0, 0].set_ylim(0, 1.5)
        axes[0, 0].text(0.5, -0.1, 'One door hides a car, two hide goats', 
                      ha='center', transform=axes[0, 0].transAxes)
        
        # Stage 2: Player makes a choice
        player_colors = door_colors.copy()
        player_colors[player_choice] = '#3498db'  # Blue for player choice
        axes[0, 1].bar(door_labels, [1, 1, 1], color=player_colors)
        axes[0, 1].set_title('Stage 2: Player Chooses a Door')
        axes[0, 1].set_ylim(0, 1.5)
        axes[0, 1].text(0.5, -0.1, f'Player chooses {door_labels[player_choice]}', 
                      ha='center', transform=axes[0, 1].transAxes)
        
        # Stage 3: Host reveals a goat
        host_colors = player_colors.copy()
        host_colors[host_reveal] = '#e74c3c'  # Red for host reveal
        axes[0, 2].bar(door_labels, [1, 1, 1], color=host_colors)
        axes[0, 2].set_title('Stage 3: Host Reveals a Goat')
        axes[0, 2].set_ylim(0, 1.5)
        axes[0, 2].text(0.5, -0.1, f'Host reveals a goat behind {door_labels[host_reveal]}', 
                      ha='center', transform=axes[0, 2].transAxes)
        
        # Stage 4a: Player stays with original choice
        final_choice_stay = player_choice
        stay_colors = host_colors.copy()
        stay_colors[final_choice_stay] = '#3498db'  # Keep blue for player's choice
        axes[1, 0].bar(door_labels, [1, 1, 1], color=stay_colors)
        axes[1, 0].set_title('Stage 4a: Player Stays with Original Choice')
        axes[1, 0].set_ylim(0, 1.5)
        axes[1, 0].text(0.5, -0.1, f'Player stays with {door_labels[final_choice_stay]}', 
                      ha='center', transform=axes[1, 0].transAxes)
        
        # Stage 4b: Player switches to other door
        final_choice_switch = [i for i in range(3) if i != player_choice and i != host_reveal][0]
        switch_colors = host_colors.copy()
        switch_colors[final_choice_switch] = '#3498db'  # Blue for new player choice
        switch_colors[player_choice] = '#f39c12'  # Original choice goes back to neutral
        axes[1, 1].bar(door_labels, [1, 1, 1], color=switch_colors)
        axes[1, 1].set_title('Stage 4b: Player Switches to Other Door')
        axes[1, 1].set_ylim(0, 1.5)
        axes[1, 1].text(0.5, -0.1, f'Player switches to {door_labels[final_choice_switch]}', 
                      ha='center', transform=axes[1, 1].transAxes)
        
        # Final result: Show where the car was
        final_colors = ['#f39c12', '#f39c12', '#f39c12']
        final_colors[car_door] = '#2ecc71'  # Green for car location
        
        axes[1, 2].bar(door_labels, [1, 1, 1], color=final_colors)
        axes[1, 2].set_title('Final: Car Location Revealed')
        axes[1, 2].set_ylim(0, 1.5)
        
        # Add text to show if each strategy would win
        stay_result = "WIN" if final_choice_stay == car_door else "LOSE"
        switch_result = "WIN" if final_choice_switch == car_door else "LOSE"
        result_text = f"Car was behind {door_labels[car_door]}\n"
        result_text += f"Stay strategy: {stay_result}\n"
        result_text += f"Switch strategy: {switch_result}"
        axes[1, 2].text(0.5, -0.1, result_text, ha='center', transform=axes[1, 2].transAxes)
        
        plt.tight_layout()
        plt.savefig('monty_hall_visualization.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return stay_result, switch_result, car_door, player_choice, host_reveal

# Run the simulator
if __name__ == "__main__":
    simulator = MontyHallSimulator()
    
    # Run simulation
    print("Running Monty Hall Problem simulation...")
    simulator.run_simulation(num_trials=10000)
    
    # Display results
    switch_wins = sum(simulator.results_switch)
    stay_wins = sum(simulator.results_stay)
    total = len(simulator.results_switch)
    
    print(f"\nResults after {total} trials:")
    print(f"Switch strategy: {switch_wins} wins ({switch_wins/total:.2%} win rate)")
    print(f"Stay strategy: {stay_wins} wins ({stay_wins/total:.2%} win rate)")
    print(f"Theoretical probabilities - Switch: 2/3 (66.67%), Stay: 1/3 (33.33%)")
    
    # Plot the results
    simulator.plot_results()
    
    # Visualize a single game state
    print("\nVisualizing a single game...")
    stay_result, switch_result, car_door, player_choice, host_reveal = simulator.visualize_game_state()
    
    # Create animation
    print("\nCreating animation of win rate convergence...")
    simulator.create_animated_simulation(num_frames=50)
    print("Animation saved as 'monty_hall_animation.gif'") 