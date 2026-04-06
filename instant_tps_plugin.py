import os
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from .instant_tps import InstantTPSDialog

class InstantTPSPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.dlg = None
        self.action = None

    def initGui(self):
        from .translations import tr
        # Crear la acción del menú/barra de herramientas
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')
        self.action = QAction(QIcon(icon_path), tr("Magic Canopy Model Generator - UAV"), self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        
        # Añadir al menú Raster de QGIS
        self.iface.addPluginToRasterMenu("&Magic Canopy Model Generator - UAV", self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        # Quitar la acción al descargar el plugin
        self.iface.removePluginRasterMenu("&Magic Canopy Model Generator - UAV", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        if not self.dlg:
            self.dlg = InstantTPSDialog(self.iface)
        
        self.dlg.show()
        self.dlg.exec_()
