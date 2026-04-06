<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/919f9fcf-076b-449e-9f2c-689d3f03fa36" />



##🛠 Installation
Download or clone this repository.
Copy the  folder into your local QGIS plugins directory: (e.g., C:\Users\YourUser\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins).

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

- First, select your Digital Surface Model from the DSM layer dropdown.
<img width="560" height="45" alt="image" src="https://github.com/user-attachments/assets/a37a6644-7e18-4305-8f03-68d0b3d5d12a" />

- Click the **"Mark Bare Soil Points"** button.
- Navigate your map and click areas where the actual soil is visible (field edges, paths, or between wide rows). 
- Each click captures the exact elevation (Z) of the terrain at that spot.
-
- <img width="890" height="886" alt="image" src="https://github.com/user-attachments/assets/c73d9d7c-2582-4693-ab92-d7cfadebd53c" />
<img width="745" height="654" alt="image" src="https://github.com/user-attachments/assets/33fb4225-cac2-4598-be59-8a40f476f963" />

Tip: For greater ease, you can use the true-color orthomosaic as a guide to place the points on bare ground (always keep in mind that you must have a DSM selected in the plugin).

<img width="626" height="398" alt="image" src="https://github.com/user-attachments/assets/2d5aa10a-b9f8-4492-a506-b96c6c86a533" />


### 4. Run the interpolation ⚡
Once you have marked the points for interpolation (we recommend ensuring sufficient representation across all areas), click "Run TPS Interpolation

The plugin uses the Thin Plate Spline (TPS) algorithm to interpolate the reference points and generate a continuous Digital Terrain Model (DTM) beneath the crop canopy.

It automatically performs **Leave-One-Out Cross-Validation (LOOCV)** to find the perfect smoothing balance, ensuring statistically sound results.

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

   <img width="561" height="170" alt="image" src="https://github.com/user-attachments/assets/edbf13a9-2c5c-4c76-a939-a3dcaede1539" />

---


