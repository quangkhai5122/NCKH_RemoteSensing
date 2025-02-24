import h5py
import pandas as pd
import os
import geopandas as gpd
from shapely.geometry import Point

shp_path = "D:\\Remote Sensing and ML\\LandMAP_Natural Earth\\ne_10m_land_clipped.shp"
folder_path = "D:\\Remote Sensing and ML\\DataCO2\\SWIRL2CO2_202301"
output_file = "xco2_data_January_2023_in_land.csv"

min_lat, max_lat = 5, 40
min_lon, max_lon = 80, 120

# Đọc dữ liệu SHP
try:
    land_gdf = gpd.read_file(shp_path)
except Exception as e:
    print(f"Lỗi khi đọc file SHP: {e}")
    exit()

all_data = []

# Duyệt qua tất cả các file .h5 trong thư mục
for filename in os.listdir(folder_path):
    if filename.endswith(".h5"):
        file_path = os.path.join(folder_path, filename)

        try:
            with h5py.File(file_path, 'r') as f:
                latitudes = f['Data/geolocation/latitude'][:]
                longitudes = f['Data/geolocation/longitude'][:]
                xco2_corrected = f['Data/mixingRatio/XCO2BiasCorrected'][:]
        except Exception as e:
            print(f"Lỗi khi đọc file HDF5 {filename}: {e}")
            continue 

        date_str = filename[9:17]
        try:
            date = pd.to_datetime(date_str, format='%Y%m%d').date()
        except ValueError:
            print(f"Lỗi định dạng ngày trong tên file: {filename}")
            continue

        data = pd.DataFrame({
            'Latitude': latitudes.flatten(),
            'Longitude': longitudes.flatten(),
            'XCO2BiasCorrected': xco2_corrected.flatten(),
            'Date': date
        })

        # Lọc theo giới hạn tọa độ
        data = data[
            (data['Latitude'] >= min_lat) & (data['Latitude'] <= max_lat) &
            (data['Longitude'] >= min_lon) & (data['Longitude'] <= max_lon)
        ]

        # Tạo GeoDataFrame
        geometry = [Point(xy) for xy in zip(data['Longitude'], data['Latitude'])]
        co2_gdf = gpd.GeoDataFrame(data, geometry=geometry, crs="EPSG:4326")

        # Tìm các điểm CO2 nằm trên đất liền
        land_points = co2_gdf[co2_gdf.intersects(land_gdf.unary_union)]

        # Lấy lại DataFrame từ GeoDataFrame đã lọc
        data_on_land = land_points.drop(columns='geometry')

        if not data_on_land.empty:
            all_data.append(data_on_land)

if all_data:
    final_data = pd.concat(all_data, ignore_index=True)
    final_data.to_csv(output_file, index=False)
    print(f"Dữ liệu đã được lưu vào file: {output_file}")
else:
    print("Không có dữ liệu nào nằm trong giới hạn tọa độ được chỉ định.")