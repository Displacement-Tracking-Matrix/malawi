import polars as pl
import geopandas as gpd
import contextily as ctx
from shapely.geometry import Point
import matplotlib.pyplot as plt

# Read in the CSV files
gis_df = pl.read_csv("../data/gis.csv")
data_df = pl.read_csv("../data/data.csv", ignore_errors=True)

# Perform left join from gis to data and add assessed column
df = gis_df.join(
    data_df,
    left_on="ADM3_CODE",  # column from gis.csv
    right_on="m0305_meta_adm3_pcode",  # column from data.csv
    how='left'
).with_columns([
    pl.when(pl.col("_uuid").is_null())
      .then(pl.lit("no"))
      .otherwise(pl.lit("yes"))
      .alias('assessed')
])

df=df.to_pandas()


# {#fig-map-coverage}

# Create geometry from latitude and longitude - using uppercase column names
geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(
    df,
    geometry=geometry,
    crs="EPSG:4326"
)

# Create figure with square dimensions
fig, ax = plt.subplots(figsize=(8, 8))

# Plot non-assessed locations in gray
non_assessed = gdf[gdf['assessed'] == "no"].to_crs(epsg=3857)
assessed = gdf[gdf['assessed'] == "yes"].to_crs(epsg=3857)

non_assessed.plot(
    ax=ax,
    color='gray',
    alpha=0.5,
    markersize=30
)

# Plot assessed locations in blue
assessed.plot(
    ax=ax,
    color='blue',
    alpha=0.5,
    markersize=30
)

# Add a positron basemap
ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, attribution=None, attribution_size=0)

# Ensure square aspect ratio
ax.set_aspect('equal')

# Adjust the plot
ax.set_axis_off()

# Add legend
ax.legend(['Non-assessed', 'Assessed'], loc='upper right')

# Use tight layout while preserving aspect ratio
plt.tight_layout()
plt.savefig('../figures/fig-map-coverage.svg', format='svg', bbox_inches='tight', dpi=300)





#{#fig-movetype}
#{#fig-map-locations-arrivals}
#{#fig-map-locations-departures}
#{#fig-map-locations-returns}
#{#fig-bar-loc-settlementtype}
#{#fig-bar-loc-urban} (appears twice)
#{#fig-bar-movetype}
#{#fig-bar-movement-type-individuals}
#{#fig-bar-movement-type-households}
#{#fig-pie-demographics}
#{#fig-pie-demographics-arrivals}
#{#fig-pie-demographics-returnees}
#{#fig-bar-pop-urban}