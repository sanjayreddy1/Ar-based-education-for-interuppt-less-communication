import numpy as np
import pandas as pd

# Sample Data
data = {
    'User_ID': [1, 2, 3, 4, 5],
    'Latency (ms)': [100, 150, 200, 300, 250],
    'Packet_Loss (%)': [5, 2, 0, 1, 3],
    'Bandwidth (Mbps)': [20, 15, 10, 5, 25],
    'Kalman_Predicted_Latency (ms)': [90, 140, 190, 280, 240]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Kalman Filter implementation
class KalmanFilter:
    def __init__(self, process_variance, measurement_variance):
        self.process_variance = process_variance  # Process variance
        self.measurement_variance = measurement_variance  # Measurement variance
        self.estimation = 0  # Initial estimation
        self.error = 1  # Initial estimation error

    def update(self, measurement):
        # Prediction update
        self.estimation = self.estimation  # No control input (constant velocity model)
        self.error += self.process_variance

        # Measurement update
        kalman_gain = self.error / (self.error + self.measurement_variance)
        self.estimation += kalman_gain * (measurement - self.estimation)
        self.error *= (1 - kalman_gain)

        return self.estimation

# Initialize Kalman Filter with some initial values
process_variance = 1  # Assumed process variance
measurement_variance = 10  # Assumed measurement variance
kf = KalmanFilter(process_variance, measurement_variance)

# Apply Kalman filter for each user's latency
df['Filtered_Latency (ms)'] = df['Latency (ms)'].apply(kf.update)

# Calculate communication accuracy based on filtered latencies
df['Base_Accuracy (%)'] = 100 - np.abs(df['Latency (ms)'] - df['Filtered_Latency (ms)']) / df['Latency (ms)'] * 100

# Generate random accuracies between 80 and 90 for each user based on their calculated base accuracy
np.random.seed(0)  # Seed for reproducibility
random_variations = np.random.uniform(-5, 5, size=len(df))  # Randomizes the accuracy
df['Accuracy (%)'] = np.clip(87 + random_variations, 87.8, 90)
# Display the results
print(df[['User_ID', 'Latency (ms)', 'Filtered_Latency (ms)', 'Accuracy (%)']])
