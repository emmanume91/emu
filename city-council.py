import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Replace these with your actual file paths
csv_file_path = 'path_to_your_csv.csv'  # Path to your CSV file
shapefile_path = 'path_to_your_shapefile.shp'  # Path to your city council districts shapefile

# Load the CSV data into a DataFrame
df = pd.read_csv(csv_file_path)

# Convert the DataFrame to a GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

# Ensure the GeoDataFrame uses the correct CRS (Coordinate Reference System)
# It's common for shapefiles to use EPSG:4326 for lat/lon data but check your shapefile's CRS
gdf.crs = "EPSG:4326"

# Load the city council districts shapefile
districts = gpd.read_file(shapefile_path)

# Perform a spatial join between the crash data and the districts
# This adds the district information to your crash data GeoDataFrame
joined_gdf = gpd.sjoin(gdf, districts, how="left", op="within")

# Assuming 'district_name' is the column in your shapefile with the district names/IDs,
# if not, replace 'district_name' with the actual column name
# This creates a new DataFrame with the district information appended
result_df = joined_gdf.drop(columns='geometry').drop(columns=['index_right'])

# Save the updated DataFrame to a new CSV file
result_df.to_csv('updated_crash_data_with_district.csv', index=False)

print("District information appended and saved to 'updated_crash_data_with_district.csv'.")
