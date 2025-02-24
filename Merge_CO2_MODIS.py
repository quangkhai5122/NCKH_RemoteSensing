import pandas as pd

# Đọc file CO2 trước
merged_df = pd.read_csv("CO2_data.csv")

# Danh sách các file cần merge
file_list = ["ndvi.csv", "evi.csv", "lst.csv"]

for file in file_list:
    df = pd.read_csv(file)
    merged_df = pd.merge(merged_df, df, on=["Latitude", "Longitude"], how="inner")

# Lưu file CSV cuối cùng
merged_df.to_csv("CO2_MODIS_Merged.csv", index=False)

print("✅ Đã ghép dữ liệu thành công!")
