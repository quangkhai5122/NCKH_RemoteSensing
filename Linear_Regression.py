import pandas as pd
import numpy as np
from scipy.stats import linregress
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

df = pd.read_csv("CO2_MODIS_Merged.csv")

# X (NDVI) và y (CO2)
X = df["NDVI"]
y = df["XCO2BiasCo"]

# HHồi quy tuyến tính
slope, intercept, r_value, p_value, std_err = linregress(X, y)

# Tính giá trị dự đoán và RMSE
y_pred = slope * X + intercept
rmse = np.sqrt(mean_squared_error(y, y_pred))

print(f"Hệ số tương quan (r): {r_value:.3f}")
print(f"RMSE: {rmse:.3f}")
print(f"p-value: {p_value:.3f}")

# Vẽ biểu đồ scatter
plt.scatter(df["NDVI"], df["XCO2BiasCo"], alpha=0.5, label="Dữ liệu thực tế")
plt.plot(X, y_pred, color='red', linewidth=2, label="Hồi quy tuyến tính") 
plt.xlabel("NDVI")
plt.ylabel("CO2 (XCO2BiasCo)")
plt.title("Mối quan hệ giữa NDVI và CO2")
plt.legend()
plt.show()
