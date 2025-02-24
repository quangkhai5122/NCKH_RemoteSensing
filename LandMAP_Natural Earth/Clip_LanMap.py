import geopandas as gpd
from shapely.geometry import Polygon

# Đọc shapefile
land_gdf = gpd.read_file("D:\\Remote Sensing and ML\\LandMAP_Natural Earth\\ne_10m_land.shp")

# Xác định vùng cần cắt (ví dụ: hình chữ nhật)
min_lon, min_lat = 80, 5  # Kinh độ và vĩ độ tối thiểu
max_lon, max_lat = 120, 40  # Kinh độ và vĩ độ tối đa

# Tạo một GeoDataFrame đại diện cho vùng cần cắt
bbox = gpd.GeoDataFrame(
    {'geometry': [Polygon([(min_lon, min_lat), (max_lon, min_lat), (max_lon, max_lat), (min_lon, max_lat)])]},
    crs=land_gdf.crs
)

# Cắt shapefile
clipped_land_gdf = gpd.clip(land_gdf, bbox)

# Lưu shapefile đã cắt (tùy chọn)
clipped_land_gdf.to_file("D:\\Remote Sensing and ML\\LandMAP_Natural Earth\\ne_10m_land_clipped.shp")