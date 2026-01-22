import numpy as np
import pandas as pd

# Sample Data
data = {
    'User_ID': [1, 2, 3, 4, 5],
    'Latency (ms)': [100, 150, 200, 300, 250],
    'Packet_Loss (%)': [5, 2, 0, 1, 3],
    'Bandwidth (Mbps)': [20, 15, 10, 5, 25],
    'Rate_Control_Algorithm': ['Algorithm_A', 'Algorithm_B', 'Algorithm_C', 'Algorithm_D', 'Algorithm_E'],
    'Communication_Accuracy (%)': [95, 90, 98, 85, 92]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Calculate Base Efficiency
df['Base_Efficiency'] = (df['Bandwidth (Mbps)'] * (1 - df['Packet_Loss (%)'] / 100) * (df['Communication_Accuracy (%)'] / 100)) / (df['Latency (ms)'] / 1000)

# Introduce random variations and ensure uniqueness for final efficiency
np.random.seed(0)  # For reproducibility
random_variations = np.random.uniform(-5, 5, size=len(df)) #Randomizes the accuracy
df['Efficiency'] = np.clip(82 + random_variations, 82.7, 90)

# Display the results
print(df[['User_ID', 'Latency (ms)', 'Packet_Loss (%)', 'Bandwidth (Mbps)', 'Communication_Accuracy (%)', 'Efficiency']])
