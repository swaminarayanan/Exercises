import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error

# =======================
# 1. Load Data
# =======================
df = pd.read_csv('/home/swami/Downloads/test_dataset.csv')

# Access individual columns
dates = df["DateTime"]
actual = df["Actual"]
model1 = df["Model_0"]
model2 = df["Model_1"]
model3 = df["Model_2"]
model4 = df["Model_3"]
model5 = df["Model_4"]
model6 = df["Model_5"]

# Optional: Sum of Model6
su = model6.sum()
print("Sum of Model6:", su)

# =======================
# 2. Create Combined DataFrame
# =======================
df_all = pd.DataFrame({
    "Date": dates,
    "Actual": actual,
    "Model1": model1,
    "Model2": model2,
    "Model3": model3,
    "Model4": model4,
    "Model5": model5,
    "Model6": model6
})

# =======================
# 3. Plot Line Comparison
# =======================
plt.figure(figsize=(12, 6))
plt.plot(df_all["Date"], df_all["Actual"], label="Actual", linewidth=2)
for i in range(1, 7):
    plt.plot(df_all["Date"], df_all[f"Model{i}"], label=f"Model{i}", linestyle="--")
plt.legend()
plt.title("Actual vs Model Data")
plt.xlabel("Date")
plt.ylabel("Value")
plt.grid()
plt.tight_layout()
plt.show()

# =======================
# 4. Compute Statistics
# =======================
def compute_stats(y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    bias = np.mean(y_pred - y_true)
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    return rmse, mae, bias, corr

# =======================
# 5. Print Results
# =======================
print("Model Comparison with Actual Data:")
print("Model\t\tRMSE\t\tMAE\t\tBias\t\tCorr")
for i in range(1, 7):
    rmse, mae, bias, corr = compute_stats(df_all["Actual"], df_all[f"Model{i}"])
    print(f"Model{i}\t\t{rmse:.2f}\t\t{mae:.2f}\t\t{bias:.2f}\t\t{corr:.2f}")
