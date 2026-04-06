
CVM (Canopy Volume Model): The calculated volume per pixel in cubic meters (m³).
<p align="center">
  <img src="icon.png" width="300">
</p><p align="center">
  <img src="icon.png" width="300">
</p>

🛠 Installation
Download or clone this repository.
Copy the microplot_generator folder into your local QGIS plugins directory: (e.g., C:\Users\YourUser\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins).

<img width="651" height="341" alt="image" src="https://github.com/user-attachments/assets/c1505953-ed6c-4040-829d-d9f848e1e73c" />
<img width="988" height="750" alt="image" src="https://github.com/user-attachments/assets/d0b5331a-b370-419e-b23d-7687c85575f0" />
<img width="839" height="262" alt="image" src="https://github.com/user-attachments/assets/08edefd0-cd5d-41db-81c7-68fe271ecb30" />

## 1. Set Up Your Scene
Open QGIS and load your Orthomosaic or **Digital Surface Model (DSM)**
### 2. Launch the Plugin 🪄
Go to the **Raster Menu** and select **`Magic Canopy Model Generator - UAV`**. A clean, intuitive interface will appear.
<img width="79" height="48" alt="image" src="https://github.com/user-attachments/assets/becb24e8-ace8-4f59-8a14-0bc18e3f8b75" />
<img width="1099" height="885" alt="image" src="https://github.com/user-attachments/assets/9256f48d-9559-4c4a-8a6c-b75cf4a4b36a" />
### 3. Mark Ground Reference Points 📌
- Click the **"Mark Bare Soil Points"** button.
- Navigate your map and click areas where the actual soil is visible (field edges, paths, or between wide rows). 
- Each click captures the exact elevation (Z) of the terrain at that spot.
-
- <img width="890" height="886" alt="image" src="https://github.com/user-attachments/assets/c73d9d7c-2582-4693-ab92-d7cfadebd53c" />
<img width="745" height="654" alt="image" src="https://github.com/user-attachments/assets/33fb4225-cac2-4598-be59-8a40f476f963" />

### 4. Run the Magic (TPS + LOOCV) ⚡
Once you have marked the points for interpolation (we recommend ensuring sufficient representation across all areas), click "Run TPS Interpolation

The plugin uses the Thin Plate Spline (TPS) algorithm to interpolate the reference points and generate a continuous Digital Terrain Model (DTM) beneath the crop canopy.

It automatically performs Leave-One-Out Cross-Validation (LOOCV) to find the perfect smoothing balance.

### 5. Analyze Your Results 📏
Once processing is complete, 3 temporary RAM layers will appear in your Layers Panel:

DTM (Digital Terrain Model): The estimated soil surface.

CHM (Canopy Height Model): The true height of your plants (DSM - DTM).

CVM (Canopy Volume Model): The calculated volume per pixel (Height × Spatial Resolution).

---
## 💾 Saving Your Work
The generated layers live in your computer's RAM for maximum speed. If you want to keep them:
1. Select your preferred **Compression** (e.g., `DEFLATE` for very small files).
2. Click the **Save** button next to each product. 
3. The exported GeoTIFF will automatically re-load into your project for further analysis.
---


