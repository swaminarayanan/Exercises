# ========================================
# Libraries
# ========================================
library(ncdf4)
library(fields)
library(terra)       # For raster operations
library(sf)          # For shapefile operations
library(RColorBrewer)

# ========================================
# Step 1: Read NetCDF Data
# ========================================
nc <- nc_open("Downloads/g4.timeAvgMap.M2T1NXAER_5_12_4_DUCMASS25.20240301-20240630.61E_5N_99E_39N.nc")
var <- ncvar_get(nc, "M2T1NXAER_5_12_4_DUCMASS25") * 10000
lat <- ncvar_get(nc, "lat")
lon <- ncvar_get(nc, "lon")
nc_close(nc)

# ========================================
# Step 2: Convert to SpatRaster
# ========================================
r <- rast(t(var), extent = c(min(lon), max(lon), min(lat), max(lat)))
crs(r) <- "EPSG:4326"  # Set WGS84 coordinate system

# ========================================
# Step 3: Read and Transform India Shapefile
# ========================================
india_shape <- st_read("work script/Admin2.shp")  # <-- Replace with correct path
st_crs(india_shape) <- 4326                       # Assign projection if missing
india_shape <- st_transform(india_shape, crs(r))  # Ensure same CRS as raster

# ========================================
# Step 4: Mask Raster with Shapefile
# ========================================
r_masked <- mask(r, vect(india_shape))

# ========================================
# Step 5: Define Axis Ticks
# ========================================
xticks <- seq(60, 100, by = 5)
yticks <- seq(5, 40, by = 5)

# ========================================
# Step 6: Set Plot Margins
# ========================================
#par(mar = c(1.8, 5, 3, 2))  # Bottom, left, top, right (increased bottom for labels)
par(mar = c(1.8, 8, 3, 2))  # Bottom, left, top, right (increased bottom for labels)

# ========================================
# Step 7: Plot Raster Without Default Axes
# ========================================
color_min <- 0
color_max <- 1.2
n_colors <- 100
break_col <- seq(color_min, color_max, length.out = 101)
image.plot(r_masked, zlim = c(0, 1.2), breaks = break_col,
           main = "Polluted India",
           col = terrain.colors(100),
           xlim = c(60, 100), ylim = c(5, 40),
           axes = FALSE,
           xlab = "Longitude", ylab = "Latitude", legend.mar = 4.5, legend.width = 1.5,
           cex.main = 1.4, legend.shrink = 0.8,     # Shrink legend height
           legend.lab = "Dust Level") 
text(x = 65.3, y = 38, labels = "(a)", font = 2, cex = 0.8)

# ========================================
# Step 9: Manually Add Axis Labels
# # ========================================
# u <- par("usr")  # Get plot boundaries
# 
# # X-axis labels (below plot)
# text(x = xticks, y = u[3] - 3,
#      labels = paste0(xticks, "°E"),
#      srt = 45, xpd = TRUE, cex = 0.7, adj = 1)
# 
# # Y-axis labels (left of plot)
# text(x = u[1] -1, y = yticks,
#      labels = paste0(yticks, "°N"),
#      srt = 0, xpd = TRUE, cex = 0.7, adj = 1)
# ##############
# ========================================
# Step 9: Add Axis Ticks and Labels
# ========================================
u <- par("usr")  # Get plot boundaries

# Add tick marks (but no labels)
axis(1, at = xticks, labels = FALSE, tck = -0.02)  # X-axis ticks
axis(2, at = yticks, labels = FALSE, tck = -0.02)  # Y-axis ticks

# Add custom tick labels manually
# X-axis labels (below plot)
text(x = xticks, y = u[3] - 3,
     labels = paste0(xticks, "°E"),
     srt = 45, xpd = TRUE, cex = 0.7, adj = 1)

# Y-axis labels (left of plot)
text(x = u[1] - 1, y = yticks,
     labels = paste0(yticks, "°N"),
     srt = 0, xpd = TRUE, cex = 0.7, adj = 1)


# ========================================
# Step 10: Add Shapefile Borders
# ========================================
plot(st_geometry(india_shape), add = TRUE, border = "black", lwd = 0.8)
