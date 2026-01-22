import pandas as pd
import numpy as np

# Set sample size
sample_size = 100

# Generate synthetic dataset
np.random.seed(42)  # For reproducibility

data = {
    "User_ID": np.arange(1, sample_size + 1),
    "Bandwidth_Allocated (Mbps)": np.random.uniform(5, 100, sample_size).round(2),
    "Packet_Loss (%)": np.random.uniform(0, 10, sample_size).round(2),
    "Latency (ms)": np.random.randint(10, 300, sample_size),
    "Throughput (Mbps)": np.random.uniform(1, 90, sample_size).round(2),
    "Jitter (ms)": np.random.uniform(0, 50, sample_size).round(2),
    "Precision (%)": np.random.uniform(87, 92, sample_size).round(2)  # Updated range for Precision
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Prevent division by zero in latency
df["Latency (ms)"] = df["Latency (ms)"].replace(0, 1e-6)

# Calculate Raw Efficiency
df["Raw_Efficiency"] = (
    (df["Throughput (Mbps)"] * df["Precision (%)"]) /
    (df["Bandwidth_Allocated (Mbps)"] * (1 + df["Packet_Loss (%)"] / 100 + df["Jitter (ms)"] / df["Latency (ms)"]))
) * 100

# Normalize Efficiency to strictly fit within 87-92%
min_eff, max_eff = 87, 92
raw_min, raw_max = df["Raw_Efficiency"].min(), df["Raw_Efficiency"].max()

if raw_min == raw_max:
    # If all raw efficiencies are the same, set to mid-range (89.5%)
    df["Efficiency (%)"] = 89.5
else:
    df["Efficiency (%)"] = min_eff + ((df["Raw_Efficiency"] - raw_min) / (raw_max - raw_min)) * (max_eff - min_eff)

# Ensure efficiency is strictly within range
df["Efficiency (%)"] = df["Efficiency (%)"].clip(lower=min_eff, upper=max_eff).round(2)

# Drop raw efficiency column
df.drop(columns=["Raw_Efficiency"], inplace=True)

# Select the desired columns without Efficiency
df = df[["User_ID", "Latency (ms)", "Bandwidth_Allocated (Mbps)", "Packet_Loss (%)", "Throughput (Mbps)", "Jitter (ms)", "Precision (%)"]]

# Save as CSV
csv_filename = "Efficiency_87-92_Corrected_No_Efficiency.csv"  # Adjusted the path for clarity
df.to_csv(csv_filename, index=False)

# Return the file path
print(csv_filename)  # Show file path for confirmation

# Display the first few rows of the DataFrame to verify
print(df.head())
