import pandas as pd
import os

# Define data suitable for a Pie Chart (Few categories, clear part-to-whole relationship)
data = {
    "Department": ["Electronics", "Clothing", "Home & Garden", "Beauty", "Sports", "Toys"],
    "Budget_Allocation": [45000, 32000, 28000, 15000, 12000, 8000]
}

df = pd.DataFrame(data)

# Define output path (Desktop/ChartYapV2)
output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sample_pie_data.csv")

# Save to CSV
df.to_csv(output_path, index=False)

print(f"Pie chart sample data generated at: {output_path}")
print(df)
