from qgis.gui import QgsMapToolEmitPoint, QgsVertexMarker
from qgis.core import QgsRaster, QgsCoordinateTransform, QgsProject, QgsMessageLog, Qgis
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QColor

class PointCaptureTool(QgsMapToolEmitPoint):
    pointCaptured = pyqtSignal(float, float, float)

    def __init__(self, canvas, layer):
        super().__init__(canvas)
        self.canvas = canvas
        self.layer = layer
        self.markers = []

    def canvasPressEvent(self, e):
        # Punto en coordenadas del mapa (canvas)
        map_point = self.toMapCoordinates(e.pos())
        
        # Transformar el punto al sistema de coordenadas de la CAPA RASTER
        try:
            xform = QgsCoordinateTransform(self.canvas.mapSettings().destinationCrs(), self.layer.crs(), QgsProject.instance())
            layer_point = xform.transform(map_point)
        except Exception as ex:
            QgsMessageLog.logMessage(f"InstantTPS - Transform error: {ex}", "InstantTPS", Qgis.Warning)
            layer_point = map_point # fallback
        
        identify_result = self.layer.dataProvider().identify(layer_point, QgsRaster.IdentifyFormatValue)
        
        z_value = 0.0
        if identify_result.isValid():
            results = identify_result.results()
            raw_z = results.get(1)
            
            if raw_z is not None:
                try:
                    z_value = float(raw_z)
                except:
                    z_value = 0.0
            else:
                # Si falló la banda 1, intentar extraer el primer valor disponible
                if results and len(results) > 0:
                    first_key = list(results.keys())[0]
                    try:
                        z_value = float(results[first_key])
                    except:
                        z_value = 0.0
            
            QgsMessageLog.logMessage(
                f"Clic → layer_pt=({layer_point.x():.2f}, {layer_point.y():.2f}) raw_z={raw_z} → Z={z_value:.4f}  capa={self.layer.name()}",
                "InstantTPS", Qgis.Info
            )
        else:
            QgsMessageLog.logMessage(
                f"Clic INVÁLIDO → layer_pt=({layer_point.x():.2f}, {layer_point.y():.2f}) — fuera del raster?  capa={self.layer.name()}",
                "InstantTPS", Qgis.Warning
            )
                        
        # Siempre dibujamos en el mapa para confirmar el clic al usuario
        marker = QgsVertexMarker(self.canvas)
        marker.setCenter(map_point)
        marker.setColor(QColor(0, 0, 255))
        marker.setIconType(QgsVertexMarker.ICON_X)
        marker.setIconSize(10)
        marker.setPenWidth(2)
        self.markers.append(marker)
        
        # Emitimos para la tabla
        self.pointCaptured.emit(layer_point.x(), layer_point.y(), z_value)

    def removeMarkerAtIndex(self, index):
        if 0 <= index < len(self.markers):
            m = self.markers.pop(index)
            self.canvas.scene().removeItem(m)

    def clearMarkers(self):
        for marker in self.markers:
            self.canvas.scene().removeItem(marker)
        self.markers = []
