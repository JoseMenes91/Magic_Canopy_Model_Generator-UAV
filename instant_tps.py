import os
import tempfile
import time
import shutil
import numpy as np
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QTableWidgetItem, QMessageBox, QFileDialog
from qgis.PyQt.QtCore import QCoreApplication, Qt
from qgis.core import QgsProject, QgsRasterLayer, QgsRaster, QgsMessageLog, Qgis
from .map_tool import PointCaptureTool
from .translations import tr

try:
    from scipy.interpolate import RBFInterpolator
    HAS_SCIPY = True
except ImportError:
    try:
        from scipy.interpolate import Rbf
        HAS_SCIPY = True
    except ImportError:
        HAS_SCIPY = False

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'instant_tps_dialog_base.ui'))


class InstantTPSDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        super(InstantTPSDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.iface = iface
        self.points = []
        self.tool = None
        # Rutas temporales de los productos generados
        self.temp_paths = {"MDT": None, "MAC": None, "MVC": None}

        # ── Traducciones de la UI ──
        self.setWindowTitle(tr("Magic Canopy Model Generator - UAV") + " 🛸")
        self.label_1.setText(tr("Capa MDS:") + " 🚁")
        self.btnCapture.setText(tr("Marcar Puntos de Suelo Desnudo"))
        self.btnUndo.setText(tr("↩ Deshacer Último"))
        self.btnDeleteSelected.setText(tr("Eliminar Seleccionado"))
        self.btnClear.setText(tr("💣 Eliminar Todos los Puntos"))
        self.btnInterpolate.setText(tr("▶ Ejecutar Interpolación TPS"))
        self.labelSaveTitle.setText(tr("💾 Guardar productos (opcional — sin guardar quedan como capas temporales):"))
        self.btnSaveMDT.setText(tr("💾 MDT (Suelo)"))
        self.btnSaveMAC.setText(tr("💾 MAC (Altura)"))
        self.btnSaveMVC.setText(tr("💾 MVC (Volumen)"))
        self.labelCompression.setText(tr("Compresión (reduce el tamaño sin modificar datos):"))
        self.comboCompression.setItemText(0, tr("DEFLATE (Muy alta compresión)"))
        self.comboCompression.setItemText(1, tr("LZW (Compresión alta)"))
        self.comboCompression.setItemText(2, tr("Sin compresión"))
        self.labelStatus.setText(tr("Listo."))
        # Traducir los headers de la tabla (asumiendo que están ahí, sino QTableWidgetItem nuevo)
        if self.tablePoints.horizontalHeaderItem(0): self.tablePoints.horizontalHeaderItem(0).setText(tr("ID"))
        if self.tablePoints.horizontalHeaderItem(1): self.tablePoints.horizontalHeaderItem(1).setText(tr("X"))
        if self.tablePoints.horizontalHeaderItem(2): self.tablePoints.horizontalHeaderItem(2).setText(tr("Y"))
        if self.tablePoints.horizontalHeaderItem(3): self.tablePoints.horizontalHeaderItem(3).setText(tr("Z (Cota)"))
        # Explicación
        self.labelExplicacion.setText(tr(self.labelExplicacion.text()))

        # ── Conexiones ──
        self.btnCapture.toggled.connect(self.toggle_capture_tool)
        self.btnUndo.clicked.connect(self.undo_last_point)
        self.btnDeleteSelected.clicked.connect(self.delete_selected_points)
        self.btnClear.clicked.connect(self.clear_all)
        self.btnInterpolate.clicked.connect(self.run_interpolation)
        self.btnSaveMDT.clicked.connect(lambda: self.save_product("MDT"))
        self.btnSaveMAC.clicked.connect(lambda: self.save_product("MAC"))
        self.btnSaveMVC.clicked.connect(lambda: self.save_product("MVC"))
        self.mMapLayerComboBox.setFilters(QgsRasterLayer.RasterLayer)

    # ══════════════════════════════════════════════════════════════════════════
    # AYUDA
    # ══════════════════════════════════════════════════════════════════════════


    # ══════════════════════════════════════════════════════════════════════════
    # CAPTURA DE PUNTOS
    # ══════════════════════════════════════════════════════════════════════════
    def toggle_capture_tool(self, checked):
        layer = self.mMapLayerComboBox.currentLayer()
        if not layer:
            QMessageBox.warning(self, tr("Atención"), tr("Seleccioná una capa MDS primero."))
            self.btnCapture.setChecked(False)
            return

        if checked:
            if self.tool:
                self.iface.mapCanvas().unsetMapTool(self.tool)
            self.tool = PointCaptureTool(self.iface.mapCanvas(), layer)
            self.tool.pointCaptured.connect(self.add_point_to_table)
            self.iface.mapCanvas().setMapTool(self.tool)
            self.labelStatus.setText(tr("📌 Clavando puntos en: {layer}").format(layer=layer.name()))
        else:
            if self.tool:
                self.iface.mapCanvas().unsetMapTool(self.tool)
            self.labelStatus.setText("")

    def add_point_to_table(self, x, y, z):
        row = self.tablePoints.rowCount()
        self.tablePoints.insertRow(row)
        self.tablePoints.setItem(row, 0, QTableWidgetItem(str(row + 1)))
        self.tablePoints.setItem(row, 1, QTableWidgetItem(f"{x:.3f}"))
        self.tablePoints.setItem(row, 2, QTableWidgetItem(f"{y:.3f}"))
        self.tablePoints.setItem(row, 3, QTableWidgetItem(f"{z:.4f}"))
        self.points.append((x, y, z))

    # ══════════════════════════════════════════════════════════════════════════
    # GESTIÓN DE PUNTOS
    # ══════════════════════════════════════════════════════════════════════════
    def undo_last_point(self):
        if not self.points:
            return
        last = self.tablePoints.rowCount() - 1
        self.tablePoints.removeRow(last)
        self.points.pop()
        if self.tool:
            self.tool.removeMarkerAtIndex(last)

    def delete_selected_points(self):
        rows = sorted(set(idx.row() for idx in self.tablePoints.selectedIndexes()), reverse=True)
        for row in rows:
            self.tablePoints.removeRow(row)
            if 0 <= row < len(self.points):
                del self.points[row]
            if self.tool:
                self.tool.removeMarkerAtIndex(row)
        for i in range(self.tablePoints.rowCount()):
            self.tablePoints.setItem(i, 0, QTableWidgetItem(str(i + 1)))

    def clear_all(self):
        self.tablePoints.setRowCount(0)
        self.points = []
        if self.tool:
            self.tool.clearMarkers()
        self.progressBar.setValue(0)
        self._disable_save_buttons()

    # ══════════════════════════════════════════════════════════════════════════
    # GUARDAR PRODUCTOS INDIVIDUALES
    # ══════════════════════════════════════════════════════════════════════════
    def _disable_save_buttons(self):
        self.btnSaveMDT.setEnabled(False)
        self.btnSaveMAC.setEnabled(False)
        self.btnSaveMVC.setEnabled(False)

    def _enable_save_buttons(self):
        self.btnSaveMDT.setEnabled(True)
        self.btnSaveMAC.setEnabled(True)
        self.btnSaveMVC.setEnabled(True)

    def save_product(self, key):
        if not hasattr(self, 'temp_paths') or key not in self.temp_paths or not self.temp_paths[key]:
            QMessageBox.warning(self, tr("Error"), tr("Primero ejecutá la interpolación."))
            return

        names = {"MDT": "MDT_Suelo", "MAC": "MAC_Altura", "MVC": "MVC_Volumen"}
        dest, _ = QFileDialog.getSaveFileName(
            self, tr("Guardar {name}").format(name=names[key]), names[key] + ".tif", "GeoTIFF (*.tif)"
        )
        if dest:
            from qgis.core import QgsRasterFileWriter, QgsRasterPipe, QgsCoordinateTransformContext, QgsProject, QgsMessageLog, Qgis
            
            # Buscar la capa exacta en el proyecto de QGIS a partir de la ruta temporal
            vsimem_path = self.temp_paths[key]
            target_layer = None
            for layer in QgsProject.instance().mapLayers().values():
                if layer.source() == vsimem_path:
                    target_layer = layer
                    break

            if not target_layer:
                QMessageBox.warning(self, tr("Error"), tr("La capa temporal fue eliminada de QGIS y no se pudo guardar."))
                return

            # Opciones de compresión según el combo
            comp_idx = self.comboCompression.currentIndex()
            if comp_idx == 0:    # DEFLATE
                create_opts = ['COMPRESS=DEFLATE', 'PREDICTOR=2', 'ZLEVEL=9']
            elif comp_idx == 1:  # LZW
                create_opts = ['COMPRESS=LZW', 'PREDICTOR=2']
            else:                # Sin compresión
                create_opts = []

            try:
                pipe = QgsRasterPipe()
                provider = target_layer.dataProvider()
                pipe.set(provider.clone())

                writer = QgsRasterFileWriter(dest)
                writer.setCreateOptions(create_opts)

                result = writer.writeRaster(
                    pipe,
                    provider.xSize(),
                    provider.ySize(),
                    provider.extent(),
                    provider.crs(),
                    QgsCoordinateTransformContext()
                )

                if result == 0: # 0 == QgsRasterFileWriter.NoError
                    QgsMessageLog.logMessage(f"Guardado exitoso vía QGIS: {dest}", "Magic Canopy Model Generator - UAV", Qgis.Info)
                    self.labelStatus.setText(tr("💾 Guardado: {name}").format(name=os.path.basename(dest)))
                    
                    # Cargar automáticamente la capa recién exportada en el mapa
                    from qgis.core import QgsRasterLayer
                    new_layer = QgsRasterLayer(dest, os.path.basename(dest))
                    if new_layer.isValid():
                        QgsProject.instance().addMapLayer(new_layer)
                else:
                    QMessageBox.critical(self, tr("Error Interno de QGIS"), tr("Falló la exportación nativa al disco (Código {}). ¿El archivo ya existe y está bloqueado o abieto?").format(result))
            except Exception as e:
                QMessageBox.critical(self, tr("Error Crítico"), tr("Excepción durante el guardado: {}").format(str(e)))

    # ══════════════════════════════════════════════════════════════════════════
    # UTILIDADES
    # ══════════════════════════════════════════════════════════════════════════
    def _update_progress(self, value, total, message=""):
        pct = int(value * 100 / total) if total > 0 else 0
        self.progressBar.setValue(pct)
        if message:
            self.labelStatus.setText(message)
        QCoreApplication.processEvents()

    # ══════════════════════════════════════════════════════════════════════════
    # INTERPOLACIÓN TPS
    # ══════════════════════════════════════════════════════════════════════════
    def run_interpolation(self):
        if not HAS_SCIPY:
            QMessageBox.critical(self, tr("Error"), tr("scipy no está disponible."))
            return
        if len(self.points) < 3:
            QMessageBox.warning(self, tr("Faltan puntos"), tr("Necesitás al menos 3 puntos."))
            return

        src_layer = self.mMapLayerComboBox.currentLayer()
        if not src_layer:
            return

        self.progressBar.setValue(0)
        self._disable_save_buttons()
        self._update_progress(0, 100, tr("Preparando interpolación..."))

        try:
            pts    = np.array(self.points)
            extent = src_layer.extent()
            cols   = src_layer.width()
            rows   = src_layer.height()
            res_x  = src_layer.rasterUnitsPerPixelX()
            res_y  = src_layer.rasterUnitsPerPixelY()

            # ── 1. NORMALIZACIÓN (R::Tps scale.type="range") ──
            x_pts_min   = pts[:, 0].min()
            x_pts_max   = pts[:, 0].max()
            y_pts_min   = pts[:, 1].min()
            y_pts_max   = pts[:, 1].max()
            x_pts_range = x_pts_max - x_pts_min
            y_pts_range = y_pts_max - y_pts_min
            if x_pts_range == 0: x_pts_range = 1.0
            if y_pts_range == 0: y_pts_range = 1.0

            x_pts_n = (pts[:, 0] - x_pts_min) / x_pts_range
            y_pts_n = (pts[:, 1] - y_pts_min) / y_pts_range
            z_pts   = pts[:, 2]

            # ── 2. GRID normalizado ──
            x_centers   = np.linspace(extent.xMinimum() + res_x / 2.0, extent.xMaximum() - res_x / 2.0, cols)
            y_centers   = np.linspace(extent.yMaximum() - res_y / 2.0, extent.yMinimum() + res_y / 2.0, rows)
            x_centers_n = (x_centers - x_pts_min) / x_pts_range
            y_centers_n = (y_centers - y_pts_min) / y_pts_range

            # ── 3. LOOCV para smoothing óptimo ──
            self._update_progress(5, 100, tr("Buscando suavizado óptimo (LOOCV)..."))

            from scipy.interpolate import RBFInterpolator
            xy_train = np.column_stack((x_pts_n, y_pts_n))
            n_pts    = len(z_pts)

            smooth_candidates = [0, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.05, 0.1, 0.5, 1.0]
            best_smooth = 0
            best_loocv  = float('inf')

            for s in smooth_candidates:
                loocv_error = 0.0
                for i in range(n_pts):
                    mask_loo = np.ones(n_pts, dtype=bool)
                    mask_loo[i] = False
                    try:
                        interp_loo = RBFInterpolator(
                            xy_train[mask_loo], z_pts[mask_loo],
                            kernel='thin_plate_spline', degree=1, smoothing=s
                        )
                        pred = interp_loo(xy_train[i:i+1])
                        loocv_error += (pred[0] - z_pts[i]) ** 2
                    except Exception:
                        loocv_error = float('inf')
                        break
                avg_error = loocv_error / n_pts
                if avg_error < best_loocv:
                    best_loocv  = avg_error
                    best_smooth = s

            QgsMessageLog.logMessage(
                f"LOOCV → smoothing={best_smooth} (error={best_loocv:.6f})",
                "InstantTPS", Qgis.Info
            )

            # ── 4. INTERPOLAR por bloques (rápido) ──
            self._update_progress(10, 100, tr("Interpolando TPS (λ={best_smooth})...").format(best_smooth=best_smooth))

            Z_interp = np.zeros((rows, cols), dtype=np.float32)
            interp = RBFInterpolator(
                xy_train, z_pts,
                kernel='thin_plate_spline', degree=1, smoothing=best_smooth
            )

            BLOCK = 100  # filas por bloque
            progress_start = 10
            progress_end   = 80

            for b_start in range(0, rows, BLOCK):
                b_end = min(b_start + BLOCK, rows)
                # Construir grid del bloque completo
                y_block = y_centers_n[b_start:b_end]
                # Meshgrid: cada fila del bloque × todas las columnas
                xx, yy = np.meshgrid(x_centers_n, y_block)
                grid_block = np.column_stack((xx.ravel(), yy.ravel()))
                result = interp(grid_block)
                Z_interp[b_start:b_end, :] = result.reshape(b_end - b_start, cols)

                pct = progress_start + int(b_end / rows * (progress_end - progress_start))
                self._update_progress(pct, 100, tr("Interpolando filas {start}-{end}/{total}...").format(start=b_start+1, end=b_end, total=rows))

            # ── 5. MÁSCARA + MAC + MVC ──
            self._update_progress(80, 100, tr("Calculando MAC y MVC..."))

            from osgeo import gdal
            ds_src     = gdal.Open(src_layer.source())
            band_src   = ds_src.GetRasterBand(1)
            nodata_src = band_src.GetNoDataValue()
            dsm_data   = band_src.ReadAsArray().astype(np.float32)

            if nodata_src is not None:
                if np.isnan(nodata_src):
                    valid_mask = ~np.isnan(dsm_data)
                else:
                    valid_mask = np.abs(dsm_data - nodata_src) > 1e-6
                Z_interp[~valid_mask] = nodata_src
            else:
                valid_mask = np.ones(dsm_data.shape, dtype=bool)

            QgsMessageLog.logMessage(
                f"MDT: min={Z_interp[valid_mask].min():.3f} max={Z_interp[valid_mask].max():.3f}",
                "InstantTPS", Qgis.Info
            )

            # MAC (Altura)
            mac_data = np.zeros_like(Z_interp)
            mac_temp = dsm_data[valid_mask] - Z_interp[valid_mask]
            mac_temp = np.maximum(mac_temp, 0.0)
            mac_data[valid_mask] = mac_temp
            if nodata_src is not None:
                mac_data[~valid_mask] = nodata_src

            # MVC (Volumen)
            pixel_area = abs(res_x * res_y)
            mvc_data = np.zeros_like(Z_interp)
            mvc_data[valid_mask] = mac_data[valid_mask] * pixel_area
            if nodata_src is not None:
                mvc_data[~valid_mask] = nodata_src

            # ── 6. CREAR CAPAS TEMPORALES EN MEMORIA (/vsimem/) ──
            self._update_progress(90, 100, tr("Cargando capas temporales..."))
            
            ts     = int(time.time())
            geo_t  = (extent.xMinimum(), res_x, 0, extent.yMaximum(), 0, -res_y)
            proj   = ds_src.GetProjection()
            driver = gdal.GetDriverByName('GTiff')
            ds_src = None



            products = [
                ("MDT", "MDT_Suelo",   Z_interp, f"instanttps_mdt_{ts}.tif"),
                ("MAC", "MAC_Altura",  mac_data,  f"instanttps_mac_{ts}.tif"),
                ("MVC", "MVC_Volumen", mvc_data,  f"instanttps_mvc_{ts}.tif"),
            ]

            for key, display_name, prod_array, fname in products:
                # Usamos vsimem puro y un sufijo visual porque QGIS censura su propio ícono para Rasters
                vsimem_path = f"/vsimem/{fname}"
                ds_out = driver.Create(vsimem_path, cols, rows, 1, gdal.GDT_Float32)
                ds_out.SetGeoTransform(geo_t)
                ds_out.SetProjection(proj)
                band_out = ds_out.GetRasterBand(1)
                if nodata_src is not None:
                    band_out.SetNoDataValue(nodata_src)
                band_out.WriteArray(prod_array)
                ds_out.FlushCache()
                band_out = None
                ds_out = None

                self.temp_paths[key] = vsimem_path

                rlayer = QgsRasterLayer(vsimem_path, display_name + " [Temporal RAM]")
                if rlayer.isValid():
                    QgsProject.instance().addMapLayer(rlayer)

            self._enable_save_buttons()
            self._update_progress(100, 100, tr("✅ ¡Listo! 3 capas temporales generadas."))

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, tr("Error Fatal"), str(e))
            self.progressBar.setValue(0)
