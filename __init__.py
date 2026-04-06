# Esta función es la que QGIS busca para inicializar el plugin
from .instant_tps_plugin import InstantTPSPlugin

def classFactory(iface):
    return InstantTPSPlugin(iface)
