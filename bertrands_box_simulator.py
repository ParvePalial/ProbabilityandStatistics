import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.animation import FuncAnimation

class BertrandsBoxSimulator:
    """
    Simulator for Bertrand's Box Paradox
    
    Problem: Three identical boxes each contain two coins. 
    Box 1: Two gold coins
    Box 2: Two silver coins
    Box 3: One gold coin and one silver coin
    
    A box is selected at random and a coin is drawn from it at random.
    Given that the coin is gold, what is the probability that the other coin in the box is also gold?
    
    The intuitive answer is 1/2, but the correct answer is 2/3.
    """
    
    def __init__(self):
        """Initialize the Bertrand's Box simulator"""
        self.results = []
        self.cumulative_probabilities = []
        
    def run_single_trial(self):
        """
        Run a single trial of the Bertrand's Box paradox
        
        Returns:
            tuple: (box_chosen, first_coin, second_coin)
                where box_chosen is the index of the selected box (0, 1, or 2)
                first_coin and second_coin are either 'G' (gold) or 'S' (silver)
        """
        # Define the boxes
        boxes = [
            ['G', 'G'],  # Box 1: Two gold coins
            ['S', 'S'],  # Box 2: Two silver coins
            ['G', 'S']   # Box 3: One gold and one silver coin
        ]
        
        # Select a box at random
        box_idx = np.random.randint(0, 3)
        selected_box = boxes[box_idx]
        
        # Select a coin at random from the box
        first_coin_idx = np.random.randint(0, 2)
        first_coin = selected_box[first_coin_idx]
        second_coin = selected_box[1 - first_coin_idx]  # The other coin
        
        return box_idx, first_coin, second_coin
    
    def run_simulation(self, num_trials=10000):
        """
        Run multiple trials of the Bertrand's Box paradox
        
        Args:
            num_trials (int): Number of trials to simulate
        """
        self.results = []
        self.cumulative_probabilities = []
        
        gold_first_count = 0  # Count of trials where the first coin is gold
        gold_second_given_gold_first = 0  # Count of trials where second coin is gold given first coin is gold
        
        for i in range(num_trials):
            box_idx, first_coin, second_coin = self.run_single_trial()
            
            # Store the result
            self.results.append((box_idx, first_coin, second_coin))
            
            # Update counts for conditional probability calculation
            if first_coin == 'G':
                gold_first_count += 1
                if second_coin == 'G':
                    gold_second_given_gold_first += 1
            
            # Calculate the conditional probability P(second coin is gold | first coin is gold)
            if gold_first_count > 0:
                prob = gold_second_given_gold_first / gold_first_count
            else:
                prob = 0
                
            self.cumulative_probabilities.append(prob)
    
    def plot_results(self):
        """Plot the results of the simulation"""
        # Count occurrences for different scenarios
        total_trials = len(self.results)
        gold_first = sum(1 for _, first, _ in self.results if first == 'G')
        gold_second_given_gold_first = sum(1 for _, first, second in self.results if first == 'G' and second == 'G')
        
        # Calculate conditional probability
        conditional_prob = gold_second_given_gold_first / gold_first if gold_first > 0 else 0
        
        # Set style
        sns.set(style="whitegrid")
        
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 1. Bar chart for probabilities
        labels = ['Theoretical', 'Simulated']
        probabilities = [2/3, conditional_prob]
        
        bars = ax1.bar(labels, probabilities, color=['#3498db', '#2ecc71'])
        ax1.set_ylim(0, 1)
        ax1.set_ylabel('Probability')
        ax1.set_title('P(Second Coin is Gold | First Coin is Gold)')
        
        # Add text labels on the bars
        for bar, prob in zip(bars, probabilities):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{prob:.4f}', ha='center', va='bottom', fontweight='bold')
        
        # 2. Line chart showing convergence
        trials = range(1, len(self.cumulative_probabilities) + 1)
        ax2.plot(trials, self.cumulative_probabilities, color='#2ecc71')
        ax2.axhline(y=2/3, linestyle='--', color='#3498db', label='Theoretical (2/3)')
        
        ax2.set_xlabel('Number of Trials')
        ax2.set_ylabel('Estimated Probability')
        ax2.set_title('Convergence of P(Second Coin is Gold | First Coin is Gold)')
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig('bertrands_box_results.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_animated_simulation(self, num_frames=100):
        """
        Create an animation showing how the probability converges over time
        
        Args:
            num_frames (int): Number of frames in the animation
        """
        # Run a simulation with more trials for the animation
        self.run_simulation(num_trials=num_frames*100)
        
        # Set up the figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Initialize line
        line, = ax.plot([], [], 'g-', lw=2, label='Simulated P(Second coin is gold | First coin is gold)')
        theoretical = ax.axhline(y=2/3, linestyle='--', color='blue', alpha=0.7, label='Theoretical (2/3)')
        naive = ax.axhline(y=1/2, linestyle=':', color='red', alpha=0.7, label='Naive guess (1/2)')
        
        # Set up plot
        ax.set_xlim(0, num_frames*100)
        ax.set_ylim(0, 1)
        ax.set_xlabel('Number of Trials')
        ax.set_ylabel('Probability')
        ax.set_title("Bertrand's Box Paradox - Probability Convergence")
        ax.legend(loc='lower right')
        ax.grid(True)
        
        # Animation function
        def animate(i):
            x = range(1, i*100 + 1)
            y = self.cumulative_probabilities[:i*100]
            line.set_data(x, y)
            return line,
        
        # Create animation
        anim = FuncAnimation(fig, animate, frames=num_frames, interval=50, blit=True)
        plt.close()  # Prevent display of static plot
        
        # Save animation
        anim.save('bertrands_box_animation.gif', writer='pillow', fps=10, dpi=80)
        
        return anim

    def visualize_box_selection(self):
        """Create a visual explanation of the Bertrand's Box paradox"""
        # Define the boxes
        boxes = [
            ['G', 'G'],  # Box 1: Two gold coins
            ['S', 'S'],  # Box 2: Two silver coins
            ['G', 'S']   # Box 3: One gold and one silver coin
        ]
        
        # Create figure with 3x2 grid of subplots
        fig, axes = plt.subplots(3, 2, figsize=(12, 12))
        
        # Box labels and colors
        box_labels = ['Box 1\n(Two Gold)', 'Box 2\n(Two Silver)', 'Box 3\n(One Gold, One Silver)']
        coin_colors = {'G': '#FFD700', 'S': '#C0C0C0'}  # Gold and Silver colors
        
        # Draw all boxes and their contents
        for i, box in enumerate(boxes):
            # Draw box
            axes[i, 0].bar(['Box'], [1], color='#f39c12', alpha=0.5, width=0.4)
            axes[i, 0].set_title(box_labels[i])
            axes[i, 0].set_ylim(0, 1.5)
            axes[i, 0].set_yticks([])
            
            # Draw coins in the box
            coin_positions = [-0.1, 0.1]
            for j, coin in enumerate(box):
                circle = plt.Circle((coin_positions[j], 0.5), 0.2, color=coin_colors[coin])
                axes[i, 0].add_artist(circle)
                axes[i, 0].text(coin_positions[j], 0.5, coin, ha='center', va='center', fontweight='bold')
        
        # Simulate drawing a gold coin from each box
        outcomes = []
        probabilities = []
        
        # For each box, calculate P(second coin is gold | first coin is gold)
        for i, box in enumerate(boxes):
            if 'G' in box:  # Box contains at least one gold coin
                # Count of gold coins in the box
                gold_count = box.count('G')
                
                # Probability of drawing a gold coin
                p_gold = gold_count / 2
                
                # If we draw a gold coin, what's the probability the other is gold?
                if gold_count == 2:  # Both coins are gold
                    p_second_gold_given_first_gold = 1.0
                elif gold_count == 1:  # One gold, one silver
                    p_second_gold_given_first_gold = 0.0
                
                outcomes.append((box_labels[i], p_gold, p_second_gold_given_first_gold))
                probabilities.append(p_gold * p_second_gold_given_first_gold)
        
        # Create table for calculations
        table_data = [
            ['Box', 'P(Draw Gold)', 'P(Second is Gold | First is Gold)', 'Joint Probability'],
            ['Box 1 (GG)', '1.0', '1.0', '1.0'],
            ['Box 2 (SS)', '0.0', 'N/A', '0.0'],
            ['Box 3 (GS)', '0.5', '0.0', '0.0']
        ]
        
        # Probability Tree Diagram on right column
        axes[0, 1].axis('off')
        axes[1, 1].axis('off')
        axes[2, 1].axis('off')
        
        # Calculate the final probability using Bayes' Theorem
        p_second_gold_given_first_gold = (1.0 * 1/3) / ((1.0 * 1/3) + (0.0 * 1/3) + (0.5 * 1/3))
        
        # Show explanation and final probability
        explanation = (
            "Bertrand's Box Paradox Explained:\n\n"
            "Three boxes with two coins each:\n"
            "- Box 1: Two gold coins (GG)\n"
            "- Box 2: Two silver coins (SS)\n"
            "- Box 3: One gold and one silver coin (GS)\n\n"
            "Question: If we select a random box and\n"
            "draw a gold coin, what's the probability\n"
            "the other coin is also gold?\n\n"
            "Solution using Bayes' Theorem:\n"
            "P(Box 1 | Gold coin) = P(Gold coin | Box 1) × P(Box 1) / P(Gold coin)\n\n"
            "P(Gold coin) = 1×(1/3) + 0×(1/3) + 0.5×(1/3) = 1/2\n\n"
            "P(Box 1 | Gold coin) = 1×(1/3) / (1/2) = 2/3\n\n"
            "Therefore, the probability the other coin is gold is 2/3."
        )
        
        axes[0, 1].text(0, 0.5, explanation, fontsize=10, va='center')
        axes[2, 1].text(0.5, 0, f"Final answer: {p_second_gold_given_first_gold:.4f} = 2/3", 
                      fontsize=14, fontweight='bold', ha='center')
        
        plt.tight_layout()
        plt.savefig('bertrands_box_visualization.png', dpi=300, bbox_inches='tight')
        plt.show()

# Run the simulator
if __name__ == "__main__":
    simulator = BertrandsBoxSimulator()
    
    # Run simulation
    print("Running Bertrand's Box paradox simulation...")
    simulator.run_simulation(num_trials=10000)
    
    # Display results
    gold_first = sum(1 for _, first, _ in simulator.results if first == 'G')
    gold_second_given_gold_first = sum(1 for _, first, second in simulator.results if first == 'G' and second == 'G')
    conditional_prob = gold_second_given_gold_first / gold_first if gold_first > 0 else 0
    
    print(f"\nResults after {len(simulator.results)} trials:")
    print(f"Number of trials where first coin is gold: {gold_first}")
    print(f"Number of trials where both coins are gold, given first coin is gold: {gold_second_given_gold_first}")
    print(f"P(Second coin is gold | First coin is gold): {conditional_prob:.4f}")
    print(f"Theoretical probability: 2/3 ≈ 0.6667")
    
    # Plot the results
    simulator.plot_results()
    
    # Visualize the box selection
    print("\nCreating visual explanation...")
    simulator.visualize_box_selection()
    
    # Create animation
    print("\nCreating animation of probability convergence...")
    simulator.create_animated_simulation(num_frames=50)
    print("Animation saved as 'bertrands_box_animation.gif'") 