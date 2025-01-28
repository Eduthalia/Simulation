import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Define simulation parameters
NUM_SIMULATIONS = 1000  # Number of Monte Carlo iterations
NUM_PRS = 50  # Number of pull requests to simulate
STRATEGIES = ["Single Reviewer", "Pair Review", "Group Review"]
REVIEWERS_PER_STRATEGY = {"Single Reviewer": 1, "Pair Review": 2, "Group Review": 3}

# Review time and defect detection rate parameters
REVIEW_TIME_MEAN = 2.3  # Mean review time (hours)
REVIEW_TIME_STD_DEV = 0.5  # Standard deviation for review time
DEFECT_DETECTION_RATE = 0.6  # Average probability of detecting a defect

# Simulation function
def simulate_strategy(num_prs, reviewers, review_time_mean, defect_rate):
    total_review_time = 0
    defects_detected = 0

    for _ in range(num_prs):
        # Simulate review time
        review_time = np.random.normal(review_time_mean, REVIEW_TIME_STD_DEV) * reviewers
        total_review_time += max(review_time, 0)  # Ensure non-negative time

        # Simulate defect detection
        defects_caught = np.random.binomial(reviewers, defect_rate)
        defects_detected += defects_caught

    return total_review_time, defects_detected

# Run the simulation
results = {strategy: {"times": [], "defects": []} for strategy in STRATEGIES}

for _ in range(NUM_SIMULATIONS):
    for strategy in STRATEGIES:
        reviewers = REVIEWERS_PER_STRATEGY[strategy]
        review_time, defects = simulate_strategy(NUM_PRS, reviewers, REVIEW_TIME_MEAN, DEFECT_DETECTION_RATE)
        results[strategy]["times"].append(review_time)
        results[strategy]["defects"].append(defects)

# Analyze results
summary = {}
for strategy in STRATEGIES:
    avg_time = np.mean(results[strategy]["times"])
    avg_defects = np.mean(results[strategy]["defects"])
    summary[strategy] = {"avg_time": avg_time, "avg_defects": avg_defects}

# Display results
print("Simulation Summary:")
for strategy, data in summary.items():
    print(f"{strategy}: Avg Time = {data['avg_time']:.2f} hrs, Avg Defects Detected = {data['avg_defects']:.2f}")

# Visualization
fig, ax = plt.subplots(1, 2, figsize=(12, 6))

# Plot average review time
avg_times = [summary[strategy]["avg_time"] for strategy in STRATEGIES]
ax[0].bar(STRATEGIES, avg_times, color="skyblue")
ax[0].set_title("Average Review Time")
ax[0].set_ylabel("Time (hours)")

# Plot average defects detected
avg_defects = [summary[strategy]["avg_defects"] for strategy in STRATEGIES]
ax[1].bar(STRATEGIES, avg_defects, color="lightcoral")
ax[1].set_title("Average Defects Detected")
ax[1].set_ylabel("Defects Detected")

plt.tight_layout()
plt.show()
