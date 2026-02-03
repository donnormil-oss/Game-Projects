import matplotlib.pyplot as plt
import numpy as np

# Define the clock signal and inputs
time = np.arange(0, 10, 1)  # Time steps
clock = [1 if i % 2 == 0 else 0 for i in time]
x = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
y = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

# Define the outputs S, C, Q (example logic for illustration purposes)
S = [(x[i] + y[i] + clock[i]) % 2 for i in range(len(time))]
C = [(x[i] + y[i] + clock[i]) // 2 for i in range(len(time))]
Q = [0] * len(time)
for i in range(1, len(time)):
    Q[i] = S[i - 1] if clock[i - 1] == 1 else Q[i - 1]

# Plot the signals
plt.figure(figsize=(10, 6))
plt.step(time, clock, label='Clock', where='post')
plt.step(time, x, label='x', where='post')
plt.step(time, y, label='y', where='post')
plt.step(time, S, label='S (Sum)', where='post')
plt.step(time, C, label='C (Carry)', where='post')
plt.step(time, Q, label='Q (Flip-Flop Output)', where='post')

# Add labels and legend
plt.xlabel('Time')
plt.ylabel('Signal Level')
plt.title('Timing Diagram')
plt.legend(loc='upper right')
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()
